import sys
import tkinter as tk

import customtkinter as ctk

from . import theme
from .data import load_data
from .pages import alerts, courses, dashboard, report, settings
from .services.alerts import fetch_alerts
from .services.pricing import PricingService
from .ui_helpers import refresh_scrollable_bg
from .widgets import NavButton, lbl


class App(ctk.CTk):
    def __init__(self, autostart=False):
        super().__init__()
        self.autostart = autostart
        self.data = load_data()
        self.current_page = "dashboard"
        self.selected_report_route_id = self.data.get("routes", [{}])[0].get("id") if self.data.get("routes") else None
        self.nav_buttons = {}
        self.page_container = None
        self.scrollable = None
        self.status_text = tk.StringVar(value="준비 완료")
        self.pricing_service = PricingService()
        self.live_price_cache = {}
        self._build()
        self.show("dashboard")
        if self.autostart:
            self.after(500, self._startup_minimize)

    def _build(self):
        self.title("FlightAlert")
        self.geometry("1320x780")
        self.minsize(1160, 700)
        self.configure(fg_color=theme.BG)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(self, width=196, fg_color=theme.SIDEBAR, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_rowconfigure(7, weight=1)

        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=16, pady=(18, 14))
        lbl(brand, "FlightAlert", size=22, weight="bold").pack(anchor="w")
        lbl(brand, "항공권 가격 모니터링", size=11, color=theme.SUB).pack(anchor="w", pady=(4, 0))

        for key, text in [
            ("dashboard", "대시보드"),
            ("courses", "코스 관리"),
            ("alerts", "가격 알림"),
            ("report", "보고서"),
            ("settings", "설정"),
        ]:
            button = NavButton(sidebar, text=text, command=lambda page=key: self.show(page))
            button.configure(height=38, font=("Malgun Gothic", 12, "bold"))
            button.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[key] = button

        ctk.CTkButton(
            sidebar,
            text="다크/라이트 전환",
            height=40,
            corner_radius=12,
            fg_color=theme.CARD3,
            hover_color=theme.CARD2,
            border_width=1,
            border_color=theme.BORDER,
            text_color=theme.TEXT,
            font=("Malgun Gothic", 12, "bold"),
            command=self._toggle_theme,
        ).pack(fill="x", padx=12, pady=(16, 0))

        status = ctk.CTkFrame(sidebar, fg_color=theme.CARD, corner_radius=16, border_width=1, border_color=theme.BORDER)
        status.pack(fill="x", padx=12, pady=(14, 14))
        lbl(status, "상태", size=11, weight="bold", color=theme.SUB).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(status, textvariable=self.status_text, text_color=theme.TEXT, font=("Malgun Gothic", 12, "bold")).pack(anchor="w", padx=12, pady=(0, 6))
        self.sb_info = lbl(status, self._refresh_sb_info(), size=11, color=theme.SUB, justify="left")
        self.sb_info.pack(anchor="w", padx=12, pady=(0, 12))

        self.page_container = ctk.CTkFrame(self, fg_color=theme.BG, corner_radius=0)
        self.page_container.grid(row=0, column=1, sticky="nsew")

    def _refresh_sb_info(self):
        routes = self.data.get("routes", [])
        favorites = sum(1 for route in routes if route.get("favorite"))
        alert_count = sum(1 for alert in fetch_alerts() if alert["active"])
        api_enabled = bool(self.data.get("settings", {}).get("amadeus_id") and self.data.get("settings", {}).get("amadeus_secret"))
        api_text = "연결됨" if api_enabled else "미설정"
        return f"등록 코스 {len(routes)}개\n즐겨찾기 {favorites}개\n활성 알림 {alert_count}개\nAPI {api_text}"

    def show(self, page_name):
        self.current_page = page_name
        self.configure(fg_color=theme.BG)
        for child in self.page_container.winfo_children():
            child.destroy()
        self.scrollable = None
        self.sb_info.configure(text=self._refresh_sb_info(), text_color=theme.SUB)
        for key, button in self.nav_buttons.items():
            button.set_active(key == page_name)

        if page_name == "dashboard":
            dashboard.render(self)
        elif page_name == "courses":
            courses.render(self)
        elif page_name == "alerts":
            alerts.render(self)
        elif page_name == "report":
            report.render(self)
        else:
            settings.render(self)

    def get_price_snapshot(self, route, prefer_live=False):
        cache_key = route["id"]
        cached_snapshot = self.live_price_cache.get(cache_key)
        if prefer_live:
            fresh_snapshot = self.pricing_service.get_snapshot(route, self.data.get("settings", {}), prefer_live=True)
            if fresh_snapshot.is_live:
                self.live_price_cache[cache_key] = fresh_snapshot
                return fresh_snapshot
            if cached_snapshot is not None:
                return cached_snapshot
            return fresh_snapshot
        return cached_snapshot or self.pricing_service.get_snapshot(route, self.data.get("settings", {}), prefer_live=False)

    def refresh_live_price(self, route_id):
        route = next((item for item in self.data.get("routes", []) if item["id"] == route_id), None)
        if route is None:
            self.status_text.set("선택한 코스를 찾지 못했습니다.")
            return
        snapshot = self.get_price_snapshot(route, prefer_live=True)
        if snapshot.is_live:
            self.status_text.set(f"{route['name']} 실시간 가격을 가져왔습니다.")
        else:
            self.status_text.set(f"{route['name']} 실시간 조회에 실패해 기존 값을 유지합니다.")
        self.show(self.current_page)

    def refresh_all_live_prices(self):
        routes = self.data.get("routes", [])
        if not routes:
            self.status_text.set("실시간으로 조회할 코스가 없습니다.")
            return
        live_count = 0
        for route in routes:
            snapshot = self.get_price_snapshot(route, prefer_live=True)
            if snapshot.is_live:
                live_count += 1
        if live_count:
            self.status_text.set(f"실시간 가격 {live_count}/{len(routes)}개를 갱신했습니다.")
        else:
            self.status_text.set("실시간 조회에 실패해 기존 값을 유지합니다.")
        self.show(self.current_page)

    def _toggle_theme(self):
        next_theme = "light" if theme.theme_name() == "dark" else "dark"
        theme.apply_palette(next_theme)
        self.status_text.set("테마를 변경했습니다.")
        self.after_idle(self._build_again)

    def _build_again(self):
        for child in self.winfo_children():
            try:
                child.destroy()
            except tk.TclError:
                pass
        self.nav_buttons = {}
        self.page_container = None
        self.scrollable = None
        self._build()
        self.show(self.current_page)

    def _scroll(self):
        self.scrollable = ctk.CTkScrollableFrame(
            self.page_container,
            fg_color=theme.BG,
            corner_radius=0,
            scrollbar_button_color=theme.CARD3,
            scrollbar_button_hover_color=theme.CARD2,
        )
        self.scrollable.pack(fill="both", expand=True)
        refresh_scrollable_bg(self.scrollable)
        return self.scrollable

    def _goto_report(self, route_id):
        self.selected_report_route_id = route_id
        self.show("report")

    def report_callback_exception(self, exc, val, tb):
        if isinstance(val, tk.TclError) and "invalid command name" in str(val):
            return
        super().report_callback_exception(exc, val, tb)

    def _startup_minimize(self):
        try:
            self.iconify()
            self.status_text.set("자동 실행으로 최소화 시작했습니다.")
        except tk.TclError:
            pass


def main():
    autostart = "--autostart" in sys.argv
    app = App(autostart=autostart)
    app.mainloop()
