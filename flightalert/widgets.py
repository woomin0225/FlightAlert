import tkinter as tk

import customtkinter as ctk

from . import theme
from .data import AIRPORTS


def lbl(parent, text, size=13, weight="normal", color=None, **kwargs):
    return ctk.CTkLabel(
        parent,
        text=text,
        text_color=color or theme.TEXT,
        font=("Malgun Gothic", size, weight),
        **kwargs,
    )


def card(parent, **kwargs):
    defaults = dict(fg_color=theme.CARD, corner_radius=18, border_width=1, border_color=theme.BORDER)
    defaults.update(kwargs)
    return ctk.CTkFrame(parent, **defaults)


def inner_card(parent, **kwargs):
    defaults = dict(fg_color=theme.CARD2, corner_radius=14, border_width=1, border_color=theme.BORDER2)
    defaults.update(kwargs)
    return ctk.CTkFrame(parent, **defaults)


def divider(parent, pady=10):
    line = ctk.CTkFrame(parent, height=1, fg_color=theme.BORDER, corner_radius=0)
    line.pack(fill="x", pady=pady)
    return line


def badge(parent, text, color):
    frame = ctk.CTkFrame(parent, fg_color=theme.badge_bg_for(color), corner_radius=999)
    ctk.CTkLabel(frame, text=text, text_color=color, font=("Malgun Gothic", 11, "bold"), padx=10, pady=3).pack()
    return frame


def metric_tile(parent, title, value, subtext="", accent=None):
    box = inner_card(parent)
    box.grid_columnconfigure(0, weight=1)
    lbl(box, title, size=11, color=theme.SUB).pack(anchor="w", padx=14, pady=(12, 4))
    lbl(box, value, size=22, weight="bold", color=accent or theme.TEXT).pack(anchor="w", padx=14)
    if subtext:
        lbl(box, subtext, size=11, color=theme.SUB).pack(anchor="w", padx=14, pady=(3, 12))
    else:
        ctk.CTkFrame(box, height=1, fg_color="transparent").pack(pady=(0, 12))
    return box


def section_header(parent, eyebrow, title, desc):
    wrap = ctk.CTkFrame(parent, fg_color="transparent")
    lbl(wrap, eyebrow, size=11, weight="bold", color=theme.BLUE).pack(anchor="w")
    lbl(wrap, title, size=24, weight="bold").pack(anchor="w", pady=(4, 2))
    lbl(wrap, desc, size=12, color=theme.SUB).pack(anchor="w")
    return wrap


class NavButton(ctk.CTkButton):
    def __init__(self, parent, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            height=42,
            corner_radius=12,
            anchor="w",
            font=("Malgun Gothic", 13, "bold"),
            fg_color=theme.CARD3,
            hover_color=theme.CARD2,
            text_color=theme.SUB,
            border_width=1,
            border_color=theme.BORDER,
        )

    def set_active(self, active):
        self.configure(
            fg_color=theme.BLUE if active else theme.CARD3,
            hover_color=theme.BLUE_H if active else theme.CARD2,
            text_color=theme.TEXT if active else theme.SUB,
            border_color=theme.BLUE if active else theme.BORDER,
        )


class AirportEntry(ctk.CTkFrame):
    def __init__(self, parent, width=160, placeholder_text="공항 검색", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.var = tk.StringVar()
        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.var,
            width=width,
            height=34,
            placeholder_text=placeholder_text,
            fg_color=theme.CARD2,
            border_color=theme.BORDER,
            text_color=theme.TEXT,
        )
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<KeyRelease>", self._on_change)
        self.entry.bind("<FocusOut>", self._schedule_close)
        self.entry.bind("<Down>", self._focus_popup)
        self.bind("<Destroy>", self._on_destroy)

        self._popup = None
        self._listbox = None
        self._close_job = None

    def get(self):
        value = self.var.get().strip().upper()
        if value in AIRPORTS:
            return value
        if " - " in value:
            code = value.split(" - ", 1)[0].strip().upper()
            if code in AIRPORTS:
                return code
        return value

    def set(self, value):
        self.var.set(value)

    def refresh_theme(self):
        self.entry.configure(fg_color=theme.CARD2, border_color=theme.BORDER, text_color=theme.TEXT)
        if self._popup and self._popup.winfo_exists():
            self._popup.configure(bg=theme.CARD)
            self._listbox.configure(
                bg=theme.CARD,
                fg=theme.TEXT,
                selectbackground=theme.BLUE,
                selectforeground=theme.TEXT,
                highlightbackground=theme.BORDER,
                highlightcolor=theme.BORDER,
            )

    def _matches(self, query):
        query = query.strip().lower()
        if not query:
            return []
        items = []
        for code, name in AIRPORTS.items():
            combined = f"{code} - {name}"
            if query in code.lower() or query in name.lower() or query in combined.lower():
                items.append(combined)
        return items[:10]

    def _on_change(self, _event=None):
        if self._close_job:
            self.after_cancel(self._close_job)
            self._close_job = None
        matches = self._matches(self.var.get())
        if matches:
            self._show_popup(matches)
        else:
            self._close_popup()

    def _show_popup(self, matches):
        if self._popup is None or not self._popup.winfo_exists():
            self._popup = tk.Toplevel(self)
            self._popup.wm_overrideredirect(True)
            self._popup.attributes("-topmost", True)
            self._listbox = tk.Listbox(
                self._popup,
                height=min(8, len(matches)),
                activestyle="none",
                relief="flat",
                bd=0,
                highlightthickness=1,
                font=("Malgun Gothic", 11),
            )
            self._listbox.pack(fill="both", expand=True)
            self._listbox.bind("<<ListboxSelect>>", self._select_current)
            self._listbox.bind("<Return>", self._select_current)
            self._listbox.bind("<Escape>", lambda _e: self._close_popup())
            self._listbox.bind("<FocusOut>", lambda _e: self._schedule_close())
        self.refresh_theme()
        self._listbox.delete(0, tk.END)
        for item in matches:
            self._listbox.insert(tk.END, item)
        self._listbox.configure(height=min(8, len(matches)))
        self._position_popup()

    def _position_popup(self):
        self.update_idletasks()
        self._popup.update_idletasks()
        width = self.entry.winfo_width()
        height = self._popup.winfo_reqheight()
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height() + 4
        screen_height = self.winfo_screenheight()
        if y + height > screen_height:
            y = self.entry.winfo_rooty() - height - 4
        self._popup.geometry(f"{width}x{height}+{x}+{y}")

    def _focus_popup(self, _event=None):
        if self._listbox and self._popup and self._popup.winfo_exists():
            self._listbox.focus_set()
            if self._listbox.size():
                self._listbox.selection_clear(0, tk.END)
                self._listbox.selection_set(0)
                self._listbox.activate(0)
        return "break"

    def _select_current(self, _event=None):
        if not self._listbox:
            return
        selection = self._listbox.curselection()
        if not selection:
            return
        self.var.set(self._listbox.get(selection[0]))
        self._close_popup()
        try:
            self.entry.focus_set()
            self.entry.icursor("end")
        except tk.TclError:
            return

    def _schedule_close(self, _event=None):
        if self._close_job:
            self.after_cancel(self._close_job)
        self._close_job = self.after(180, self._close_popup)

    def _close_popup(self):
        self._close_job = None
        if self._popup and self._popup.winfo_exists():
            try:
                self._popup.destroy()
            except tk.TclError:
                pass
        self._popup = None
        self._listbox = None

    def _on_destroy(self, _event=None):
        if self._close_job:
            try:
                self.after_cancel(self._close_job)
            except tk.TclError:
                pass
            self._close_job = None
        self._close_popup()
