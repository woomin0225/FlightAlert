import calendar
from datetime import date, datetime, timedelta

import numpy as np

from . import theme
from .data import ADV_DAYS, ADV_FACTORS, BASE_PRICES, DOW_FACTORS


def price_history(base_price, seed=0, days=60):
    rng = np.random.default_rng(seed)
    today = datetime.now()
    dates = []
    prices = []
    for offset in range(days, 0, -1):
        day = today - timedelta(days=offset)
        value = int(base_price * DOW_FACTORS[day.weekday()] * (1 + rng.normal(0, 0.025)))
        dates.append(day)
        prices.append(value)
    return dates, prices


def build_route_mock_data(route):
    route_id = route["id"]
    current_price = BASE_PRICES.get(route_id, 1_700_000)
    dates, history = price_history(current_price, seed=route_id)
    avg7 = float(np.mean(history[-7:])) if history else float(current_price)
    avg14 = float(np.mean(history[-14:])) if history else float(current_price)
    rng = np.random.default_rng(route_id + 17)
    weekday_prices = [
        int(current_price * factor * (1 + rng.normal(0, 0.014 + idx * 0.001)))
        for idx, factor in enumerate(DOW_FACTORS)
    ]
    return {
        "current_price": current_price,
        "dates": dates,
        "history": history,
        "sparkline": history[-14:],
        "avg7": avg7,
        "avg14": avg14,
        "avg60": int(np.mean(history)),
        "pct_change": ((current_price - avg7) / avg7 * 100) if avg7 else 0.0,
        "weekday_prices": weekday_prices,
        "best_weekday": int(np.argmin(weekday_prices)),
        "chart_low": min(min(history), min(weekday_prices)),
        "chart_high": max(max(history), max(weekday_prices)),
    }


def month_price_map(route, year, month):
    current_price = BASE_PRICES.get(route["id"], 1_700_000)
    rng = np.random.default_rng(route["id"] * 1000 + year * 100 + month)
    _, last_day = calendar.monthrange(year, month)
    prices = {}
    for day_number in range(1, last_day + 1):
        current = date(year, month, day_number)
        advance_days = max((current - date.today()).days, 0)
        adv_factor = np.interp(
            advance_days,
            ADV_DAYS,
            ADV_FACTORS,
            left=ADV_FACTORS[0],
            right=ADV_FACTORS[-1],
        )
        prices[current] = int(
            current_price
            * DOW_FACTORS[current.weekday()]
            * adv_factor
            * (1 + rng.normal(0, 0.018))
        )
    return prices


def mix_hex_colors(start_hex, end_hex, ratio):
    ratio = max(0.0, min(1.0, ratio))
    start = tuple(int(start_hex[i : i + 2], 16) for i in (1, 3, 5))
    end = tuple(int(end_hex[i : i + 2], 16) for i in (1, 3, 5))
    mixed = tuple(round(s + (e - s) * ratio) for s, e in zip(start, end))
    return "#{:02x}{:02x}{:02x}".format(*mixed)


def heatmap_cell_color(price, low, high):
    ratio = 0.5 if high <= low else (price - low) / (high - low)
    cool = mix_hex_colors(theme.CARD2, theme.GREEN, 0.20 if theme.theme_name() == "light" else 0.28)
    warm = mix_hex_colors(theme.CARD2, theme.RED, 0.20 if theme.theme_name() == "light" else 0.28)
    return mix_hex_colors(cool, warm, ratio)


def parse_time_text(value):
    try:
        return datetime.strptime(value, "%H:%M")
    except Exception:
        return None


def flight_duration_text(segment):
    start = parse_time_text(segment.get("time_from", ""))
    end = parse_time_text(segment.get("time_to", ""))
    if not start or not end:
        return "시간 미정"
    minutes = int((end - start).total_seconds() // 60)
    if minutes <= 0:
        minutes += 24 * 60
    hours, mins = divmod(minutes, 60)
    return f"{hours}시간 {mins:02d}분"
