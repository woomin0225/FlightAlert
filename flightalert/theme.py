import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


for _font_name in ["Malgun Gothic", "AppleGothic", "NanumGothic"]:
    try:
        fm.findfont(fm.FontProperties(family=_font_name), fallback_to_default=False)
        plt.rcParams["font.family"] = _font_name
        break
    except Exception:
        pass
plt.rcParams["axes.unicode_minus"] = False

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

PALETTES = {
    "dark": dict(
        BG="#07070e", SIDEBAR="#050509", CARD="#0d0d1f",
        CARD2="#13132a", CARD3="#191935",
        BORDER="#1e1e40", BORDER2="#252550",
        BLUE="#3b82f6", BLUE_H="#2563eb", BLUE_DIM="#1d3461",
        TEAL="#2dd4bf", GREEN="#22c55e", RED="#f43f5e",
        AMBER="#f59e0b", PURPLE="#a78bfa",
        TEXT="#f1f5f9", SUB="#8892a4", MUTED="#2e3454",
        CHART_BG="#0a0a1e", CHART_GRID="#181838", CHART_TEXT="#94a3b8",
    ),
    "light": dict(
        BG="#f0f4ff", SIDEBAR="#e4e9f7", CARD="#ffffff",
        CARD2="#eef1fa", CARD3="#eaedfa",
        BORDER="#c4cae0", BORDER2="#b0b8d8",
        BLUE="#2563eb", BLUE_H="#1d4ed8", BLUE_DIM="#dbeafe",
        TEAL="#0d9488", GREEN="#16a34a", RED="#dc2626",
        AMBER="#d97706", PURPLE="#7c3aed",
        TEXT="#0f172a", SUB="#334155", MUTED="#cbd5e1",
        CHART_BG="#f8faff", CHART_GRID="#e2e8f0", CHART_TEXT="#475569",
    ),
}

_BADGE_BG = {}
_THEME = "light"

BG = SIDEBAR = CARD = CARD2 = CARD3 = None
BORDER = BORDER2 = None
BLUE = BLUE_H = BLUE_DIM = None
TEAL = GREEN = RED = AMBER = PURPLE = None
TEXT = SUB = MUTED = None
CHART_BG = CHART_GRID = CHART_TEXT = None


def apply_palette(mode: str) -> None:
    global _THEME, _BADGE_BG
    global BG, SIDEBAR, CARD, CARD2, CARD3, BORDER, BORDER2
    global BLUE, BLUE_H, BLUE_DIM, TEAL, GREEN, RED, AMBER, PURPLE
    global TEXT, SUB, MUTED, CHART_BG, CHART_GRID, CHART_TEXT

    _THEME = mode
    palette = PALETTES[mode]
    BG = palette["BG"]
    SIDEBAR = palette["SIDEBAR"]
    CARD = palette["CARD"]
    CARD2 = palette["CARD2"]
    CARD3 = palette["CARD3"]
    BORDER = palette["BORDER"]
    BORDER2 = palette["BORDER2"]
    BLUE = palette["BLUE"]
    BLUE_H = palette["BLUE_H"]
    BLUE_DIM = palette["BLUE_DIM"]
    TEAL = palette["TEAL"]
    GREEN = palette["GREEN"]
    RED = palette["RED"]
    AMBER = palette["AMBER"]
    PURPLE = palette["PURPLE"]
    TEXT = palette["TEXT"]
    SUB = palette["SUB"]
    MUTED = palette["MUTED"]
    CHART_BG = palette["CHART_BG"]
    CHART_GRID = palette["CHART_GRID"]
    CHART_TEXT = palette["CHART_TEXT"]
    if mode == "dark":
        _BADGE_BG = {"BLUE": "#1a2f5a", "TEAL": "#0f3330", "GREEN": "#0f2e1a", "RED": "#3a0f1a", "AMBER": "#3a2a0a", "PURPLE": "#2a1f4a"}
    else:
        _BADGE_BG = {"BLUE": "#dbeafe", "TEAL": "#ccfbf1", "GREEN": "#dcfce7", "RED": "#fee2e2", "AMBER": "#fef3c7", "PURPLE": "#ede9fe"}
    ctk.set_appearance_mode(mode)


def badge_bg_for(color: str) -> str:
    for key, value in {"BLUE": BLUE, "TEAL": TEAL, "GREEN": GREEN, "RED": RED, "AMBER": AMBER, "PURPLE": PURPLE}.items():
        if color == value:
            return _BADGE_BG.get(key, CARD3)
    return CARD3


def theme_name() -> str:
    return _THEME


apply_palette("light")
