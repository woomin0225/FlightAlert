import tkinter as tk

import customtkinter as ctk

from .. import theme
from ..services.alerts import create_alert, disable_alert, fetch_alerts
from ..widgets import card, inner_card, lbl, section_header


def render(app):
    root = app._scroll()
    header = section_header(
        root,
        "Alerts",
        "가격 알림",
        "노선별 목표가 알림을 한 화면에서 등록하고 관리할 수 있습니다.",
    )
    header.pack(fill="x", padx=22, pady=(18, 14))

    _alert_form(app, root).pack(fill="x", padx=22, pady=(0, 14))
    _alert_list(app, root).pack(fill="both", expand=True, padx=22, pady=(0, 22))


def _alert_form(app, parent):
    routes = app.data.get("routes", [])
    box = card(parent)
    lbl(box, "새 알림 만들기", size=18, weight="bold").pack(anchor="w", padx=16, pady=(14, 4))
    lbl(box, "이메일과 목표가만 입력하면 현재 코스 기준으로 알림을 등록합니다.", size=11, color=theme.SUB).pack(anchor="w", padx=16, pady=(0, 10))

    form = ctk.CTkFrame(box, fg_color="transparent")
    form.pack(fill="x", padx=16, pady=(0, 8))
    form.grid_columnconfigure((0, 1, 2), weight=1)

    route_names = [route["name"] for route in routes] or ["등록된 코스 없음"]
    selected_route = tk.StringVar(value=route_names[0])
    email_default = app.data.get("settings", {}).get("email", "")
    email_var = tk.StringVar(value=email_default)
    target_var = tk.StringVar(value="")
    current_price_text = tk.StringVar(value="현재가 정보를 불러오는 중입니다." if routes else "등록된 코스가 없습니다.")
    message = lbl(box, "", size=11, color=theme.SUB)

    _field(form, "코스", 0, 0)
    route_menu = ctk.CTkOptionMenu(
        form,
        values=route_names,
        variable=selected_route,
        height=34,
        fg_color=theme.CARD3,
        button_color=theme.BLUE,
        button_hover_color=theme.BLUE_H,
        dropdown_fg_color=theme.CARD,
        dropdown_text_color=theme.TEXT,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 11),
    )
    route_menu.grid(row=1, column=0, sticky="ew", padx=6)

    _field(form, "이메일", 0, 1)
    ctk.CTkEntry(
        form,
        textvariable=email_var,
        height=34,
        fg_color=theme.CARD2,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
        placeholder_text="알림 수신 이메일",
    ).grid(row=1, column=1, sticky="ew", padx=6)

    _field(form, "목표가 (KRW)", 0, 2)
    ctk.CTkEntry(
        form,
        textvariable=target_var,
        height=34,
        fg_color=theme.CARD2,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
        placeholder_text="예: 1450000",
    ).grid(row=1, column=2, sticky="ew", padx=6)

    hint_box = inner_card(box)
    hint_box.pack(fill="x", padx=16, pady=(0, 12))
    lbl(hint_box, "추천 목표가", size=10, color=theme.SUB).pack(anchor="w", padx=12, pady=(10, 2))
    ctk.CTkLabel(
        hint_box,
        textvariable=current_price_text,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 11, "bold"),
        justify="left",
    ).pack(anchor="w", padx=12, pady=(0, 10))

    def update_target_suggestion(*_args):
        route = next((item for item in routes if item["name"] == selected_route.get()), None)
        if route is None:
            current_price_text.set("등록된 코스가 없습니다.")
            target_var.set("")
            return
        snapshot = app.get_price_snapshot(route, prefer_live=False)
        suggested = int(snapshot.current_price * 0.94)
        current_price_text.set(
            f"현재 기준가 ₩{int(snapshot.current_price):,}\n추천 목표가 ₩{suggested:,} ({'실시간' if snapshot.is_live else 'mock'} 기준)"
        )
        if not target_var.get().strip():
            target_var.set(str(suggested))

    selected_route.trace_add("write", update_target_suggestion)
    update_target_suggestion()

    footer = ctk.CTkFrame(box, fg_color="transparent")
    footer.pack(fill="x", padx=16, pady=(0, 16))
    message.pack(in_=footer, side="left")

    def submit():
        if not routes:
            message.configure(text="먼저 코스를 등록해 주세요.", text_color=theme.RED)
            return
        route = next((item for item in routes if item["name"] == selected_route.get()), None)
        if route is None:
            message.configure(text="선택한 코스를 찾지 못했습니다.", text_color=theme.RED)
            return
        email = email_var.get().strip()
        if not email:
            message.configure(text="이메일을 입력해 주세요.", text_color=theme.RED)
            return
        try:
            target_price = float(target_var.get().replace(",", "").strip())
        except ValueError:
            message.configure(text="목표가는 숫자로 입력해 주세요.", text_color=theme.RED)
            return

        create_alert(email, route, target_price)
        app.status_text.set("가격 알림을 등록했습니다.")
        app.show("alerts")

    ctk.CTkButton(
        footer,
        text="알림 저장",
        height=36,
        width=120,
        corner_radius=10,
        fg_color=theme.BLUE,
        hover_color=theme.BLUE_H,
        font=("Malgun Gothic", 12, "bold"),
        command=submit,
    ).pack(side="right")

    return box


def _alert_list(app, parent):
    wrap = ctk.CTkFrame(parent, fg_color="transparent")
    lbl(wrap, "등록된 알림", size=16, weight="bold").pack(anchor="w", pady=(0, 8))

    alerts = fetch_alerts()
    if not alerts:
        empty = card(wrap)
        empty.pack(fill="x")
        lbl(empty, "등록된 알림이 없습니다.", size=15, weight="bold").pack(anchor="w", padx=16, pady=(16, 4))
        lbl(empty, "대시보드나 이 화면에서 첫 알림을 만들어 보세요.", size=11, color=theme.SUB).pack(anchor="w", padx=16, pady=(0, 16))
        return wrap

    for alert in alerts:
        item = card(wrap)
        item.pack(fill="x", pady=6)
        top = ctk.CTkFrame(item, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(12, 8))
        left = ctk.CTkFrame(top, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        lbl(left, f"{alert['origin']} → {alert['destination']}", size=16, weight="bold").pack(anchor="w")
        lbl(left, f"{alert['departure_date']} · 목표가 ₩{int(alert['target_price']):,} · {alert['email']}", size=11, color=theme.SUB).pack(anchor="w", pady=(2, 0))

        status_box = inner_card(left)
        status_box.pack(anchor="w", pady=(8, 0))
        lbl(
            status_box,
            "활성" if alert["active"] else "비활성",
            size=10,
            weight="bold",
            color=theme.GREEN if alert["active"] else theme.SUB,
        ).pack(padx=10, pady=6)

        action_text = "비활성화" if alert["active"] else "닫기"
        ctk.CTkButton(
            top,
            text=action_text,
            width=92,
            height=32,
            corner_radius=10,
            fg_color=theme.CARD3,
            hover_color=theme.CARD2,
            border_width=1,
            border_color=theme.BORDER,
            text_color=theme.TEXT,
            font=("Malgun Gothic", 11, "bold"),
            command=lambda aid=alert["id"]: _disable_and_refresh(app, aid),
        ).pack(side="right")

    return wrap


def _disable_and_refresh(app, alert_id):
    disable_alert(alert_id)
    app.status_text.set("알림을 비활성화했습니다.")
    app.show("alerts")


def _field(parent, text, row, column):
    lbl(parent, text, size=11, color=theme.SUB).grid(row=row, column=column, sticky="w", padx=6, pady=(0, 4))
