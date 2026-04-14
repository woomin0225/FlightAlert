import customtkinter as ctk

from .. import theme
from ..data import AIRPORTS
from ..mock_data import build_route_mock_data
from ..ui_helpers import create_sparkline, flight_timeline
from ..widgets import card, inner_card, lbl, section_header


def render(app):
    root = app._scroll()

    header_wrap = ctk.CTkFrame(root, fg_color="transparent")
    header_wrap.pack(fill="x", padx=18, pady=(14, 10))
    header = section_header(
        header_wrap,
        "Dashboard",
        "가격 모니터링 대시보드",
        "왕복 코스는 각 편 가격을 타임라인 옆에 붙여 한눈에 비교할 수 있게 정리했습니다.",
    )
    header.pack(side="left", fill="x", expand=True)
    ctk.CTkButton(
        header_wrap,
        text="전체 실시간 갱신",
        height=36,
        corner_radius=12,
        fg_color=theme.TEAL,
        hover_color=theme.BLUE_H,
        font=("Malgun Gothic", 11, "bold"),
        command=app.refresh_all_live_prices,
    ).pack(side="right")

    routes = app.data.get("routes", [])
    grid = ctk.CTkFrame(root, fg_color="transparent")
    grid.pack(fill="both", expand=True, padx=18, pady=(0, 18))
    grid.grid_columnconfigure((0, 1), weight=1, uniform="route")

    if not routes:
        empty = card(grid, corner_radius=16)
        empty.grid(row=0, column=0, sticky="nsew")
        lbl(empty, "등록된 코스가 없습니다.", size=18, weight="bold").pack(anchor="w", padx=22, pady=(24, 6))
        lbl(empty, "코스 관리에서 새 코스를 만들면 대시보드가 채워집니다.", size=12, color=theme.SUB).pack(anchor="w", padx=22, pady=(0, 24))
        return

    for index, route in enumerate(routes):
        row = index // 2
        column = index % 2
        _dash_card(app, grid, route).grid(row=row, column=column, sticky="nsew", padx=6, pady=6)


def _dash_card(app, parent, route):
    mock = build_route_mock_data(route)
    snapshot = app.get_price_snapshot(route, prefer_live=False)
    first_segment = route["segments"][0]
    delta = mock["pct_change"]
    delta_text = f"{'▼' if delta <= 0 else '▲'} {abs(delta):.1f}%"
    delta_color = theme.TEAL if delta <= 0 else theme.RED

    shell = card(parent, corner_radius=16)
    shell.grid_columnconfigure(0, weight=1)

    top = ctk.CTkFrame(shell, fg_color="transparent")
    top.pack(fill="x", padx=14, pady=(12, 6))
    left = ctk.CTkFrame(top, fg_color="transparent")
    left.pack(side="left", fill="x", expand=True)
    lbl(left, route.get("name", "새 코스"), size=16, weight="bold").pack(anchor="w")
    lbl(
        left,
        f"{AIRPORTS.get(first_segment['origin'], first_segment['origin'])} → {AIRPORTS.get(first_segment['destination'], first_segment['destination'])}",
        size=10,
        color=theme.SUB,
    ).pack(anchor="w", pady=(2, 0))

    right = ctk.CTkFrame(top, fg_color="transparent")
    right.pack(side="right", anchor="ne")
    lbl(right, f"총액 ₩{int(snapshot.current_price):,}", size=19, weight="bold").pack(anchor="e")
    lbl(right, delta_text, size=10, weight="bold", color=delta_color).pack(anchor="e", pady=(1, 0))

    segments = route.get("segments", [])
    if segments:
        flight_timeline(
            shell,
            segments[0],
            bg_color=theme.CARD2,
            compact=True,
            price_text=f"₩{int(snapshot.outbound_price):,}" if snapshot.outbound_price is not None else None,
        ).pack(fill="x", padx=14, pady=(0, 6))
    if len(segments) > 1:
        flight_timeline(
            shell,
            segments[-1],
            bg_color=theme.CARD2,
            compact=True,
            price_text=f"₩{int(snapshot.inbound_price):,}" if snapshot.inbound_price is not None else None,
        ).pack(fill="x", padx=14, pady=(0, 6))

    spark_wrap = inner_card(shell, corner_radius=12)
    spark_wrap.pack(fill="x", padx=14, pady=(2, 12))
    spark_wrap.grid_columnconfigure(0, weight=1)
    top_row = ctk.CTkFrame(spark_wrap, fg_color="transparent")
    top_row.pack(fill="x", padx=10, pady=(8, 1))
    lbl(top_row, "최근 14일 가격 추이", size=10, weight="bold").pack(side="left")
    lbl(top_row, snapshot.message, size=9, color=theme.SUB).pack(side="right")
    canvas, widget = create_sparkline(spark_wrap, mock["sparkline"], snapshot.current_price)
    widget.pack(fill="x", padx=8, pady=(0, 6))
    widget._spark_canvas = canvas

    btn_row = ctk.CTkFrame(shell, fg_color="transparent")
    btn_row.pack(fill="x", padx=14, pady=(0, 12))
    ctk.CTkButton(
        btn_row,
        text="실시간 조회",
        height=32,
        width=88,
        corner_radius=10,
        font=("Malgun Gothic", 11, "bold"),
        fg_color=theme.TEAL,
        hover_color=theme.BLUE_H,
        command=lambda rid=route["id"]: app.refresh_live_price(rid),
    ).pack(side="left")
    ctk.CTkButton(
        btn_row,
        text="가격 알림",
        height=32,
        width=88,
        corner_radius=10,
        font=("Malgun Gothic", 11, "bold"),
        fg_color=theme.CARD3,
        hover_color=theme.CARD2,
        border_width=1,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
        command=lambda: app.show("alerts"),
    ).pack(side="left", padx=(6, 0))
    ctk.CTkButton(
        btn_row,
        text="보고서",
        height=32,
        width=78,
        corner_radius=10,
        font=("Malgun Gothic", 11, "bold"),
        fg_color=theme.BLUE,
        hover_color=theme.BLUE_H,
        command=lambda rid=route["id"]: app._goto_report(rid),
    ).pack(side="left", padx=(6, 0))

    return shell
