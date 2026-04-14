import tkinter as tk

import customtkinter as ctk

from .. import theme
from ..data import DOW_KR, save_data
from ..services.startup import disable_startup, enable_startup, is_startup_enabled, startup_supported
from ..widgets import card, inner_card, lbl, section_header


def render(app):
    root = app._scroll()
    settings = app.data.setdefault("settings", {})

    header = section_header(
        root,
        "Settings",
        "환경 설정",
        "API와 알림 설정, 자동 실행 옵션을 한 곳에서 관리할 수 있습니다.",
    )
    header.pack(fill="x", padx=18, pady=(14, 10))

    body = ctk.CTkFrame(root, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=18, pady=(0, 8))
    body.grid_columnconfigure((0, 1), weight=1, uniform="settings")

    email_var = tk.StringVar(value=settings.get("email", ""))
    time_var = tk.StringVar(value=settings.get("send_time", "09:00"))
    amadeus_id_var = tk.StringVar(value=settings.get("amadeus_id", ""))
    amadeus_secret_var = tk.StringVar(value=settings.get("amadeus_secret", ""))
    amadeus_env_var = tk.StringVar(value=settings.get("amadeus_env", "test"))
    startup_var = tk.BooleanVar(value=settings.get("run_on_startup", is_startup_enabled()))
    day_vars = {day: tk.BooleanVar(value=day in settings.get("send_days", [])) for day in DOW_KR}

    mail_card = card(body, corner_radius=16)
    mail_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
    lbl(mail_card, "알림 설정", size=16, weight="bold").pack(anchor="w", padx=14, pady=(12, 8))
    _entry_row(mail_card, "수신 이메일", email_var, placeholder="example@email.com")
    _entry_row(mail_card, "발송 시간", time_var, placeholder="09:00")

    day_box = inner_card(mail_card, corner_radius=12)
    day_box.pack(fill="x", padx=14, pady=(0, 10))
    lbl(day_box, "발송 요일", size=10, color=theme.SUB).pack(anchor="w", padx=10, pady=(8, 4))
    row = ctk.CTkFrame(day_box, fg_color="transparent")
    row.pack(fill="x", padx=8, pady=(0, 8))
    for day in DOW_KR:
        ctk.CTkCheckBox(
            row,
            text=day,
            variable=day_vars[day],
            checkbox_width=14,
            checkbox_height=14,
            border_color=theme.BORDER2,
            fg_color=theme.BLUE,
            hover_color=theme.BLUE_H,
            text_color=theme.TEXT,
            font=("Malgun Gothic", 10),
        ).pack(side="left", padx=(0, 8))

    startup_box = inner_card(mail_card, corner_radius=12)
    startup_box.pack(fill="x", padx=14, pady=(0, 14))
    lbl(startup_box, "자동 실행", size=10, color=theme.SUB).pack(anchor="w", padx=10, pady=(8, 4))
    ctk.CTkCheckBox(
        startup_box,
        text="컴퓨터 켜질 때 FlightAlert 자동 시작",
        variable=startup_var,
        checkbox_width=14,
        checkbox_height=14,
        border_color=theme.BORDER2,
        fg_color=theme.BLUE,
        hover_color=theme.BLUE_H,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 10),
    ).pack(anchor="w", padx=8, pady=(0, 4))
    if startup_supported():
        lbl(startup_box, "자동 실행 시 프로그램은 최소화된 상태로 시작되어 성능 영향이 매우 적습니다.", size=9, color=theme.SUB).pack(anchor="w", padx=10, pady=(0, 8))
    else:
        lbl(startup_box, "현재 환경에서는 자동 실행 등록을 지원하지 않습니다.", size=9, color=theme.RED).pack(anchor="w", padx=10, pady=(0, 8))

    api_card = card(body, corner_radius=16)
    api_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
    lbl(api_card, "Amadeus API", size=16, weight="bold").pack(anchor="w", padx=14, pady=(12, 8))
    _entry_row(api_card, "Client ID", amadeus_id_var, placeholder="API Client ID")
    _entry_row(api_card, "Client Secret", amadeus_secret_var, placeholder="API Client Secret", show="*")

    env_box = inner_card(api_card, corner_radius=12)
    env_box.pack(fill="x", padx=14, pady=(0, 14))
    lbl(env_box, "환경", size=10, color=theme.SUB).pack(anchor="w", padx=10, pady=(8, 4))
    ctk.CTkSegmentedButton(
        env_box,
        values=["test", "production"],
        variable=amadeus_env_var,
        height=28,
        selected_color=theme.BLUE,
        selected_hover_color=theme.BLUE_H,
        unselected_color=theme.CARD3,
        unselected_hover_color=theme.CARD2,
        fg_color=theme.CARD2,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 10, "bold"),
    ).pack(anchor="w", padx=10, pady=(0, 10))

    footer = ctk.CTkFrame(root, fg_color=theme.BG)
    footer.pack(fill="x", padx=18, pady=(0, 16))
    footer.grid_columnconfigure(0, weight=1)
    status = lbl(footer, "", size=10, color=theme.SUB)
    status.grid(row=0, column=0, sticky="w")

    def persist_settings():
        settings["email"] = email_var.get().strip()
        settings["send_time"] = time_var.get().strip()
        settings["send_days"] = [day for day, var in day_vars.items() if var.get()]
        settings["amadeus_id"] = amadeus_id_var.get().strip()
        settings["amadeus_secret"] = amadeus_secret_var.get().strip()
        settings["amadeus_env"] = amadeus_env_var.get().strip()
        settings["run_on_startup"] = bool(startup_var.get())
        save_data(app.data)
        app.live_price_cache.clear()

    def apply_startup_setting():
        if not startup_supported():
            return False, "이 환경에서는 자동 실행 설정을 지원하지 않습니다."
        if startup_var.get():
            return enable_startup()
        return disable_startup()

    def save_all():
        persist_settings()
        ok, startup_message = apply_startup_setting()
        app.status_text.set("설정을 저장했습니다." if ok else startup_message)
        status.configure(
            text="모든 설정이 저장되었습니다. " + startup_message,
            text_color=theme.TEAL if ok else theme.RED,
        )

    def test_connection():
        persist_settings()
        ok, message = app.pricing_service.test_connection(app.data.get("settings", {}))
        app.status_text.set(message)
        status.configure(text=message, text_color=theme.TEAL if ok else theme.RED)

    ctk.CTkButton(
        footer,
        text="연결 테스트",
        height=38,
        width=120,
        corner_radius=12,
        fg_color=theme.CARD3,
        hover_color=theme.CARD2,
        border_width=1,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 11, "bold"),
        command=test_connection,
    ).grid(row=0, column=1, sticky="e", padx=(0, 8))

    ctk.CTkButton(
        footer,
        text="모두 저장",
        height=38,
        width=120,
        corner_radius=12,
        fg_color=theme.BLUE,
        hover_color=theme.BLUE_H,
        font=("Malgun Gothic", 11, "bold"),
        command=save_all,
    ).grid(row=0, column=2, sticky="e")


def _entry_row(parent, title, variable, placeholder="", show=None):
    box = inner_card(parent, corner_radius=12)
    box.pack(fill="x", padx=14, pady=(0, 10))
    lbl(box, title, size=10, color=theme.SUB).pack(anchor="w", padx=10, pady=(8, 3))
    ctk.CTkEntry(
        box,
        textvariable=variable,
        height=32,
        show=show,
        placeholder_text=placeholder,
        fg_color=theme.CARD3,
        border_color=theme.BORDER,
        text_color=theme.TEXT,
    ).pack(fill="x", padx=10, pady=(0, 10))
