from backend.db import add_alert, deactivate_alert, init_db, list_alerts


def ensure_alert_db():
    init_db()


def fetch_alerts():
    ensure_alert_db()
    return list_alerts()


def create_alert(email, route, target_price, currency="KRW"):
    ensure_alert_db()
    segment = route.get("segments", [{}])[0]
    add_alert(
        email=email,
        origin=segment.get("origin", ""),
        destination=segment.get("destination", ""),
        departure_date=segment.get("date", ""),
        target_price=float(target_price),
        adults=int(route.get("adults", 1)),
        currency=currency,
    )


def disable_alert(alert_id):
    ensure_alert_db()
    deactivate_alert(alert_id)
