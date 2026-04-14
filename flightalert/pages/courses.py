from datetime import date, timedelta
import tkinter as tk

import customtkinter as ctk

from .. import theme
from ..data import AIRPORTS, BAG_PRICES, save_data
from ..ui_helpers import flight_timeline
from ..widgets import AirportEntry, badge, card, inner_card, lbl, section_header


def render(app):
    root = app._scroll()
    header = section_header(
        root,
        "Courses",
        "코스 관리",
        "13인치 노트북에서도 한 번에 더 많은 코스를 볼 수 있도록 입력 폼과 리스트 밀도를 높였습니다.",
    )
    header.pack(fill="x", padx=18, pady=(14, 10))

    _course_add_form(app, root).pack(fill="x", padx=18, pady=(0, 10))
    _course_list(app, root).pack(fill="both", expand=True, padx=18, pady=(0, 18))


def _course_add_form(app, parent):
    box = card(parent, corner_radius=16)
    box.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    lbl(box, "새 코스 만들기", size=16, weight="bold").grid(row=0, column=0, columnspan=5, sticky="w", padx=14, pady=(12, 3))
    lbl(box, "필수 항목만 빠르게 저장할 수 있는 압축 폼입니다.", size=10, color=theme.SUB).grid(row=1, column=0, columnspan=5, sticky="w", padx=14, pady=(0, 8))

    name_var = tk.StringVar(value=f"코스 {len(app.data.get('routes', [])) + 1}")
    type_var = tk.StringVar(value="왕복")
    adults_var = tk.StringVar(value="1")
    bag_var = tk.StringVar(value=list(BAG_PRICES)[1])
    favorite_var = tk.BooleanVar(value=True)
    depart_var = tk.StringVar(value=(date.today() + timedelta(days=30)).isoformat())
    return_var = tk.StringVar(value=(date.today() + timedelta(days=37)).isoformat())

    origin_entry = AirportEntry(box, width=128, placeholder_text="출발지")
    destination_entry = AirportEntry(box, width=128, placeholder_text="도착지")

    _field(box, "코스명", 2, 0)
    ctk.CTkEntry(box, textvariable=name_var, height=32, fg_color=theme.CARD2, border_color=theme.BORDER, text_color=theme.TEXT).grid(row=3, column=0, sticky="ew", padx=5)
    _field(box, "출발지", 2, 1)
    origin_entry.grid(row=3, column=1, sticky="ew", padx=5)
    _field(box, "도착지", 2, 2)
    destination_entry.grid(row=3, column=2, sticky="ew", padx=5)
    _field(box, "출발일", 2, 3)
    ctk.CTkEntry(box, textvariable=depart_var, height=32, fg_color=theme.CARD2, border_color=theme.BORDER, text_color=theme.TEXT).grid(row=3, column=3, sticky="ew", padx=5)
    _field(box, "귀국일", 2, 4)
    return_entry = ctk.CTkEntry(box, textvariable=return_var, height=32, fg_color=theme.CARD2, border_color=theme.BORDER, text_color=theme.TEXT)
    return_entry.grid(row=3, column=4, sticky="ew", padx=5)

    control_row = ctk.CTkFrame(box, fg_color="transparent")
    control_row.grid(row=4, column=0, columnspan=5, sticky="ew", padx=5, pady=(8, 0))
    control_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

    type_box = inner_card(control_row, corner_radius=12)
    type_box.grid(row=0, column=0, sticky="ew", padx=(0, 3))
    lbl(type_box, "여행", size=10, color=theme.SUB).pack(anchor="w", padx=8, pady=(6, 2))
    ctk.CTkSegmentedButton(
        type_box,
        values=["왕복", "편도"],
        variable=type_var,
        height=28,
        selected_color=theme.BLUE,
        selected_hover_color=theme.BLUE_H,
        unselected_color=theme.CARD3,
        unselected_hover_color=theme.CARD2,
        fg_color=theme.CARD2,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 10, "bold"),
        command=lambda value: _toggle_return_state(value, return_entry),
    ).pack(fill="x", padx=6, pady=(0, 6))

    adults_box = inner_card(control_row, corner_radius=12)
    adults_box.grid(row=0, column=1, sticky="ew", padx=3)
    lbl(adults_box, "인원", size=10, color=theme.SUB).pack(anchor="w", padx=8, pady=(6, 2))
    ctk.CTkOptionMenu(
        adults_box,
        variable=adults_var,
        values=["1", "2", "3", "4"],
        height=28,
        fg_color=theme.CARD3,
        button_color=theme.BLUE,
        button_hover_color=theme.BLUE_H,
        dropdown_fg_color=theme.CARD,
        text_color=theme.TEXT,
        dropdown_text_color=theme.TEXT,
        font=("Malgun Gothic", 10),
    ).pack(fill="x", padx=6, pady=(0, 6))

    bag_box = inner_card(control_row, corner_radius=12)
    bag_box.grid(row=0, column=2, sticky="ew", padx=3)
    lbl(bag_box, "수하물", size=10, color=theme.SUB).pack(anchor="w", padx=8, pady=(6, 2))
    ctk.CTkOptionMenu(
        bag_box,
        variable=bag_var,
        values=list(BAG_PRICES),
        height=28,
        fg_color=theme.CARD3,
        button_color=theme.BLUE,
        button_hover_color=theme.BLUE_H,
        dropdown_fg_color=theme.CARD,
        text_color=theme.TEXT,
        dropdown_text_color=theme.TEXT,
        font=("Malgun Gothic", 10),
    ).pack(fill="x", padx=6, pady=(0, 6))

    favorite_box = inner_card(control_row, corner_radius=12)
    favorite_box.grid(row=0, column=3, sticky="ew", padx=(3, 0))
    lbl(favorite_box, "표시", size=10, color=theme.SUB).pack(anchor="w", padx=8, pady=(6, 2))
    ctk.CTkCheckBox(
        favorite_box,
        text="즐겨찾기",
        variable=favorite_var,
        checkbox_width=14,
        checkbox_height=14,
        border_color=theme.BORDER2,
        fg_color=theme.BLUE,
        hover_color=theme.BLUE_H,
        text_color=theme.TEXT,
        font=("Malgun Gothic", 10),
    ).pack(anchor="w", padx=6, pady=(0, 7))

    footer = ctk.CTkFrame(box, fg_color="transparent")
    footer.grid(row=5, column=0, columnspan=5, sticky="ew", padx=14, pady=(8, 12))
    message = lbl(footer, "", size=10, color=theme.SUB)
    message.pack(side="left")

    def save_course():
        origin = origin_entry.get()
        destination = destination_entry.get()
        if origin not in AIRPORTS or destination not in AIRPORTS:
            message.configure(text="출발지와 도착지는 목록에서 선택해 주세요.", text_color=theme.RED)
            return

        route_id = max((route["id"] for route in app.data.get("routes", [])), default=0) + 1
        segments = [{
            "origin": origin,
            "destination": destination,
            "date": depart_var.get().strip(),
            "time_from": "09:00",
            "time_to": "12:00",
            "arr_time": "12:00",
        }]
        if type_var.get() == "왕복":
            segments.append({
                "origin": destination,
                "destination": origin,
                "date": return_var.get().strip(),
                "time_from": "13:00",
                "time_to": "16:00",
                "arr_time": "16:00",
            })

        app.data.setdefault("routes", []).append({
            "id": route_id,
            "name": name_var.get().strip() or f"코스 {route_id}",
            "trip_type": type_var.get(),
            "segments": segments,
            "adults": int(adults_var.get() or "1"),
            "baggage": bag_var.get(),
            "favorite": bool(favorite_var.get()),
        })
        save_data(app.data)
        app.status_text.set("새 코스를 저장했습니다.")
        app.show("courses")

    ctk.CTkButton(
        footer,
        text="저장",
        height=32,
        width=90,
        corner_radius=10,
        fg_color=theme.BLUE,
        hover_color=theme.BLUE_H,
        font=("Malgun Gothic", 11, "bold"),
        command=save_course,
    ).pack(side="right")

    _toggle_return_state(type_var.get(), return_entry)
    return box


def _course_list(app, parent):
    wrap = ctk.CTkFrame(parent, fg_color="transparent")
    lbl(wrap, "등록된 코스", size=15, weight="bold").pack(anchor="w", pady=(0, 6))

    routes = app.data.get("routes", [])
    if not routes:
        empty = card(wrap, corner_radius=16)
        empty.pack(fill="x")
        lbl(empty, "아직 코스가 없습니다.", size=14, weight="bold").pack(anchor="w", padx=14, pady=(14, 4))
        lbl(empty, "위 폼에서 첫 번째 코스를 만들어 보세요.", size=10, color=theme.SUB).pack(anchor="w", padx=14, pady=(0, 14))
        return wrap

    for route in routes:
        item = card(wrap, corner_radius=16)
        item.pack(fill="x", pady=5)

        top = ctk.CTkFrame(item, fg_color="transparent")
        top.pack(fill="x", padx=12, pady=(10, 6))
        left = ctk.CTkFrame(top, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        lbl(left, route.get("name", "코스"), size=15, weight="bold").pack(anchor="w")
        lbl(left, f"{route.get('trip_type', '편도')} · 성인 {route.get('adults', 1)}명 · {route.get('baggage', '-')}", size=10, color=theme.SUB).pack(anchor="w", pady=(1, 0))
        if route.get("favorite"):
            badge(left, "즐겨찾기", theme.BLUE).pack(anchor="w", pady=(6, 0))

        actions = ctk.CTkFrame(top, fg_color="transparent")
        actions.pack(side="right")
        ctk.CTkButton(actions, text="보고서", width=68, height=30, corner_radius=10, fg_color=theme.CARD3, hover_color=theme.CARD2, border_width=1, border_color=theme.BORDER, text_color=theme.TEXT, font=("Malgun Gothic", 10, "bold"), command=lambda rid=route["id"]: app._goto_report(rid)).pack(side="left")
        ctk.CTkButton(actions, text="삭제", width=62, height=30, corner_radius=10, fg_color=theme.RED, hover_color=theme.RED, text_color="#ffffff", font=("Malgun Gothic", 10, "bold"), command=lambda rid=route["id"]: _delete_route(app, rid)).pack(side="left", padx=(6, 0))

        for segment in route.get("segments", []):
            flight_timeline(item, segment, bg_color=theme.CARD2, compact=True).pack(fill="x", padx=12, pady=(0, 6))

    return wrap


def _delete_route(app, route_id):
    app.data["routes"] = [route for route in app.data.get("routes", []) if route["id"] != route_id]
    app.live_price_cache.pop(route_id, None)
    save_data(app.data)
    app.status_text.set("코스를 삭제했습니다.")
    app.show("courses")


def _field(parent, text, row, column):
    lbl(parent, text, size=10, color=theme.SUB).grid(row=row, column=column, sticky="w", padx=5, pady=(0, 3))


def _toggle_return_state(value, widget):
    widget.configure(state="normal" if value == "왕복" else "disabled")
