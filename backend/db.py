import os
import sqlite3
from datetime import datetime

from flightalert.paths import app_base_dir

DB_PATH = os.path.join(app_base_dir(), "alerts.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            adults INTEGER DEFAULT 1,
            target_price REAL NOT NULL,
            currency TEXT DEFAULT 'KRW',
            last_notified TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def get_active_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM alerts WHERE active = 1").fetchall()
    conn.close()
    return rows


def add_alert(email, origin, destination, departure_date, target_price, adults=1, currency="KRW"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO alerts (email, origin, destination, departure_date, target_price, adults, currency)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (email, origin, destination, departure_date, target_price, adults, currency),
    )
    conn.commit()
    conn.close()


def update_last_notified(alert_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE alerts SET last_notified = ? WHERE id = ?",
        (datetime.now().isoformat(), alert_id),
    )
    conn.commit()
    conn.close()


def list_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM alerts").fetchall()
    conn.close()
    return rows


def deactivate_alert(alert_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE alerts SET active = 0 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
