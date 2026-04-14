from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import customtkinter as ctk

from . import theme
from .mock_data import flight_duration_text
from .widgets import lbl


def refresh_scrollable_bg(scrollable):
    scrollable.configure(fg_color=theme.BG)
    for attr in ("_parent_frame", "_parent_canvas", "_scrollbar"):
        widget = getattr(scrollable, attr, None)
        if widget is None:
            continue
        try:
            if attr == "_scrollbar":
                widget.configure(button_color=theme.CARD3, button_hover_color=theme.CARD2, fg_color=theme.BG)
            elif attr == "_parent_canvas":
                widget.configure(bg=theme.BG, highlightthickness=0)
            else:
                widget.configure(fg_color=theme.BG)
        except Exception:
            pass


def create_sparkline(parent, prices, current_price):
    line_color = theme.TEAL if current_price <= (sum(prices) / max(len(prices), 1)) else theme.RED
    figure = Figure(figsize=(3.2, 0.62), dpi=100)
    figure.patch.set_alpha(0)
    axis = figure.add_subplot(111)
    axis.set_facecolor("none")
    axis.plot(prices, color=line_color, linewidth=1.7)
    axis.scatter([len(prices) - 1], [prices[-1]], color=line_color, s=10, zorder=3)
    axis.set_xticks([])
    axis.set_yticks([])
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.margins(x=0.03, y=0.28)
    figure.subplots_adjust(left=0, right=1, top=1, bottom=0)

    canvas = FigureCanvasTkAgg(figure, master=parent)
    widget = canvas.get_tk_widget()
    widget.configure(bg=theme.CARD2, highlightthickness=0, bd=0)
    canvas.draw()
    return canvas, widget


def flight_timeline(parent, segment, bg_color=None, compact=False, price_text=None):
    bg_color = bg_color or theme.CARD2
    shell_width = 312 if compact else 396
    left_width = 42 if compact else 54
    center_width = 132 if compact else 184
    right_width = 42 if compact else 54
    meta_width = 144 if compact else 176
    row_height = 58 if compact else 70

    outer = ctk.CTkFrame(parent, fg_color="transparent")
    outer.grid_columnconfigure(0, weight=0)
    outer.grid_columnconfigure(1, weight=1)

    shell = ctk.CTkFrame(
        outer,
        width=shell_width,
        height=row_height,
        fg_color=bg_color,
        corner_radius=10 if compact else 12,
        border_width=1,
        border_color=theme.BORDER2,
    )
    shell.grid(row=0, column=0, sticky="w")
    shell.grid_propagate(False)

    content = ctk.CTkFrame(shell, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=(8 if compact else 12), pady=(6 if compact else 8))
    content.grid_columnconfigure(0, minsize=left_width)
    content.grid_columnconfigure(1, minsize=center_width)
    content.grid_columnconfigure(2, minsize=right_width)

    left = ctk.CTkFrame(content, fg_color="transparent", width=left_width)
    left.grid(row=0, column=0, sticky="nw")
    left.grid_propagate(False)
    lbl(left, segment.get("origin", "---"), size=13 if compact else 14, weight="bold").pack(anchor="w")
    lbl(left, segment.get("time_from", "--:--"), size=10 if compact else 11, color=theme.SUB).pack(anchor="w", pady=(5 if compact else 7, 0))

    center = ctk.CTkFrame(content, fg_color="transparent", width=center_width)
    center.grid(row=0, column=1, padx=(10, 10), sticky="ew")
    center.grid_propagate(False)
    canvas = ctk.CTkCanvas(
        center,
        width=center_width,
        height=18 if compact else 22,
        bg=bg_color,
        highlightthickness=0,
        bd=0,
    )
    canvas.pack(fill="x", pady=(2, 0))
    _draw_timeline(canvas, center_width, compact)
    lbl(center, flight_duration_text(segment), size=9 if compact else 10, color=theme.SUB).pack(pady=(2, 0))

    right = ctk.CTkFrame(content, fg_color="transparent", width=right_width)
    right.grid(row=0, column=2, sticky="ne")
    right.grid_propagate(False)
    lbl(right, segment.get("destination", "---"), size=13 if compact else 14, weight="bold").pack(anchor="e")
    lbl(right, segment.get("arr_time", segment.get("time_to", "--:--")), size=10 if compact else 11, color=theme.SUB).pack(anchor="e", pady=(5 if compact else 7, 0))

    if price_text:
        meta = ctk.CTkFrame(
            outer,
            width=meta_width,
            height=row_height,
            fg_color=theme.CARD3,
            corner_radius=10 if compact else 12,
            border_width=1,
            border_color=theme.BORDER,
        )
        meta.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        meta.configure(width=meta_width)
        info = ctk.CTkFrame(meta, fg_color="transparent")
        info.pack(fill="both", expand=True, padx=8, pady=6)
        info.grid_columnconfigure((0, 1, 2), weight=1, uniform="meta")
        _meta_cell(info, 0, "출발", segment.get("time_from", "--:--"), compact)
        _meta_cell(info, 1, "도착", segment.get("arr_time", segment.get("time_to", "--:--")), compact)
        _meta_cell(info, 2, "금액", price_text, compact, value_color=theme.BLUE)

    return outer


def _meta_cell(parent, column, label_text, value_text, compact, value_color=None):
    cell = ctk.CTkFrame(parent, fg_color="transparent")
    cell.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 4, 0))
    lbl(cell, label_text, size=8 if compact else 9, color=theme.SUB).pack(anchor="w")
    lbl(cell, value_text, size=9 if compact else 10, weight="bold", color=value_color or theme.TEXT).pack(anchor="w", pady=(2, 0))


def _draw_timeline(canvas, width, compact):
    canvas.delete("all")
    width = max(width, 120)
    mid_y = 9 if compact else 11
    start_x = 8
    end_x = width - 8
    plane_x = (start_x + end_x) / 2
    color = theme.BLUE
    dash = 3 if compact else 4
    canvas.create_line(start_x, mid_y, plane_x - 8, mid_y, fill=color, width=2)
    canvas.create_line(plane_x + 8, mid_y, end_x, mid_y, fill=color, width=2, dash=(dash, dash))
    canvas.create_text(plane_x, mid_y, text="✈", fill=color, font=("Malgun Gothic", 11 if compact else 12, "bold"))
