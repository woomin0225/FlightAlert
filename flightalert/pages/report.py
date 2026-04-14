import calendar
from datetime import date

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .. import theme
from ..data import AIRPORTS
from ..mock_data import build_route_mock_data, heatmap_cell_color, month_price_map
from ..ui_helpers import flight_timeline
from ..widgets import card, inner_card, lbl, section_header


def render(app):
    root = app._scroll()
    routes = app.data.get("routes", [])
    route = next((item for item in routes if item["id"] == app.selected_report_route_id), None)
    if route is None and routes:
        route = routes[0]
        app.selected_report_route_id = route["id"]

    header = section_header(
        root,
        "Report",
        "노선 보고서",
        "대시보드와 같은 기준으로 출발편, 귀국편, 총액을 분리해 확인할 수 있습니다.",
    )
    header.pack(fill="x", padx=18, pady=(14, 10))

    if not routes:
        empty = card(root, corner_radius=16)
        empty.pack(fill="x", padx=18, pady=(0, 18))
        lbl(empty, "보고서를 볼 코스가 없습니다.", size=16, weight="bold").pack(anchor="w", padx=16, pady=(16, 6))
        lbl(empty, "코스 관리에서 새 코스를 만든 뒤 다시 확인해 주세요.", size=11, color=theme.SUB).pack(anchor="w", padx=16, pady=(0, 16))
        return

    selector_card = card(root, corner_radius=16)
    selector_card.pack(fill="x", padx=18, pady=(0, 10))
    lbl(selector_card, "보고서 코스 선택", size=13, weight="bold").pack(anchor="w", padx=14, pady=(12, 6))
    selector = ctk.CTkSegmentedButton(
        selector_card,
        values=[route_item["name"] for route_item in routes],
        selected_color=theme.BLUE,
        selected_hover_color=theme.BLUE_H,
        unselected_color=theme.CARD3,
        unselected_hover_color=theme.CARD2,
        fg_color=theme.CARD2,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 10, "bold"),
        command=lambda name: _select_route(app, routes, name),
    )
    selector.pack(fill="x", padx=14, pady=(0, 12))
    selector.set(route["name"])

    _render_report(app, root, route)


def _select_route(app, routes, name):
    route = next((item for item in routes if item["name"] == name), None)
    if route:
        app.selected_report_route_id = route["id"]
        app.show("report")


def _render_report(app, parent, route):
    mock = build_route_mock_data(route)
    snapshot = app.get_price_snapshot(route, prefer_live=False)

    summary = card(parent, corner_radius=16)
    summary.pack(fill="x", padx=18, pady=(0, 10))
    summary.grid_columnconfigure(0, weight=3)
    summary.grid_columnconfigure(1, weight=2)

    info = ctk.CTkFrame(summary, fg_color="transparent")
    info.grid(row=0, column=0, sticky="nsew", padx=(14, 8), pady=12)
    first_segment = route["segments"][0]
    lbl(info, route["name"], size=18, weight="bold").pack(anchor="w")
    lbl(info, f"{AIRPORTS.get(first_segment['origin'], first_segment['origin'])} → {AIRPORTS.get(first_segment['destination'], first_segment['destination'])}", size=11, color=theme.SUB).pack(anchor="w", pady=(2, 6))

    segments = route.get("segments", [])
    if segments:
        flight_timeline(
            info,
            segments[0],
            bg_color=theme.CARD2,
            compact=True,
            price_text=f"₩{int(snapshot.outbound_price):,}" if snapshot.outbound_price is not None else None,
        ).pack(fill="x", pady=(6, 0))
    if len(segments) > 1:
        flight_timeline(
            info,
            segments[-1],
            bg_color=theme.CARD2,
            compact=True,
            price_text=f"₩{int(snapshot.inbound_price):,}" if snapshot.inbound_price is not None else None,
        ).pack(fill="x", pady=(6, 0))

    actions = ctk.CTkFrame(info, fg_color="transparent")
    actions.pack(anchor="w", pady=(10, 0))
    ctk.CTkButton(
        actions,
        text="실시간 다시 조회",
        height=32,
        corner_radius=10,
        fg_color=theme.TEAL,
        hover_color=theme.BLUE_H,
        font=("Malgun Gothic", 11, "bold"),
        command=lambda rid=route["id"]: app.refresh_live_price(rid),
    ).pack(side="left")

    metrics = ctk.CTkFrame(summary, fg_color="transparent")
    metrics.grid(row=0, column=1, sticky="nsew", padx=(8, 14), pady=12)
    metrics.grid_columnconfigure((0, 1), weight=1, uniform="report")
    _metric(metrics, 0, 0, "출발편", snapshot.outbound_price)
    _metric(metrics, 0, 1, "귀국편", snapshot.inbound_price)
    _metric(metrics, 1, 0, "총액", snapshot.current_price, accent=theme.BLUE)
    _metric(metrics, 1, 1, "7일 평균 대비", mock["pct_change"], is_percent=True, accent=theme.TEAL if mock["pct_change"] <= 0 else theme.RED)

    tabs = ctk.CTkTabview(
        parent,
        fg_color=theme.CARD,
        segmented_button_fg_color=theme.CARD2,
        segmented_button_selected_color=theme.BLUE,
        segmented_button_selected_hover_color=theme.BLUE_H,
        segmented_button_unselected_color=theme.CARD3,
        text_color=theme.TEXT,
    )
    tabs.pack(fill="both", expand=True, padx=18, pady=(0, 18))
    tabs.add("추세 차트")
    tabs.add("최저가 달력")
    tabs.tab("추세 차트").configure(fg_color=theme.CARD)
    tabs.tab("최저가 달력").configure(fg_color=theme.CARD)

    _render_report_charts(tabs.tab("추세 차트"), snapshot, mock)
    _render_calendar_heatmap(tabs.tab("최저가 달력"), route)


def _metric(parent, row, column, title, value, is_percent=False, accent=None):
    box = inner_card(parent, corner_radius=12)
    box.grid(row=row, column=column, padx=4, pady=4, sticky="nsew")
    lbl(box, title, size=9, color=theme.SUB).pack(anchor="w", padx=10, pady=(8, 1))
    if is_percent:
        value_text = f"{value:+.1f}%"
    else:
        value_text = "-" if value is None else f"₩{int(value):,}"
    lbl(box, value_text, size=15, weight="bold", color=accent or theme.TEXT).pack(anchor="w", padx=10, pady=(0, 8))


def _render_report_charts(parent, snapshot, mock):
    panel = card(parent, corner_radius=16)
    panel.pack(fill="both", expand=True, padx=6, pady=6)

    figure = Figure(figsize=(7.6, 3.0), dpi=100)
    figure.patch.set_facecolor(theme.CHART_BG)
    axis = figure.add_subplot(111)
    axis.set_facecolor(theme.CHART_BG)
    axis.plot(mock["dates"], mock["history"], color=theme.BLUE, linewidth=1.8, label="일별 추이")
    axis.axhline(mock["avg7"], color=theme.TEAL, linewidth=1.3, linestyle="--", label="7일 평균")
    axis.axhline(snapshot.current_price, color=theme.RED if mock["pct_change"] > 0 else theme.TEAL, linewidth=1.2, linestyle=":", label=f"{snapshot.provider} 총액")
    axis.grid(color=theme.CHART_GRID, linewidth=0.8, alpha=0.9)
    axis.tick_params(colors=theme.CHART_TEXT, labelsize=8)
    for spine in axis.spines.values():
        spine.set_color(theme.CHART_GRID)
    axis.set_title("최근 60일 가격 흐름", color=theme.TEXT, fontsize=12, fontweight="bold")
    axis.legend(facecolor=theme.CARD, edgecolor=theme.BORDER, labelcolor=theme.TEXT, fontsize=8)
    figure.autofmt_xdate()

    canvas = FigureCanvasTkAgg(figure, master=panel)
    widget = canvas.get_tk_widget()
    widget.configure(bg=theme.CHART_BG, highlightthickness=0, bd=0)
    widget.pack(fill="both", expand=True, padx=10, pady=10)
    canvas.draw()


def _render_calendar_heatmap(parent, route):
    panel = card(parent, corner_radius=16)
    panel.pack(fill="both", expand=True, padx=6, pady=6)

    today = date.today()
    prices = month_price_map(route, today.year, today.month)
    low = min(prices.values())
    high = max(prices.values())

    lbl(panel, f"{today.year}년 {today.month}월 예상 최저가 달력", size=14, weight="bold").pack(anchor="w", padx=14, pady=(12, 3))
    lbl(panel, "낮은 가격은 초록색, 높은 가격은 빨간색으로 표시됩니다.", size=10, color=theme.SUB).pack(anchor="w", padx=14, pady=(0, 10))

    grid = ctk.CTkFrame(panel, fg_color="transparent")
    grid.pack(fill="both", expand=True, padx=12, pady=(0, 12))
    for column in range(7):
        grid.grid_columnconfigure(column, weight=1, uniform="calendar")

    for idx, day_name in enumerate(["월", "화", "수", "목", "금", "토", "일"]):
        head = inner_card(grid, corner_radius=10)
        head.grid(row=0, column=idx, sticky="ew", padx=2, pady=(0, 3))
        lbl(head, day_name, size=10, weight="bold", color=theme.SUB).pack(pady=4)

    month_rows = calendar.monthcalendar(today.year, today.month)
    for row_index, week in enumerate(month_rows, start=1):
        for col_index, day_number in enumerate(week):
            if day_number == 0:
                ctk.CTkFrame(grid, fg_color="transparent").grid(row=row_index, column=col_index, sticky="nsew", padx=2, pady=2)
                continue
            current = date(today.year, today.month, day_number)
            value = prices[current]
            cell = ctk.CTkFrame(grid, fg_color=heatmap_cell_color(value, low, high), corner_radius=10, border_width=1, border_color=theme.BORDER2)
            cell.grid(row=row_index, column=col_index, sticky="nsew", padx=2, pady=2)
            lbl(cell, str(day_number), size=11, weight="bold").pack(anchor="nw", padx=8, pady=(6, 1))
            lbl(cell, f"₩{value // 1000:,}k", size=9, weight="bold").pack(anchor="w", padx=8)
