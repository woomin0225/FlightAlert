from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from amadeus_client import get_lowest_price
from config import CHECK_INTERVAL_HOURS
from db import get_active_alerts, update_last_notified
from notifier import send_alert_email


def check_prices():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 가격 확인 시작")
    alerts = get_active_alerts()

    if not alerts:
        print("활성화된 알림이 없습니다.")
        return

    for alert in alerts:
        if alert["last_notified"]:
            last = datetime.fromisoformat(alert["last_notified"])
            if datetime.now() - last < timedelta(hours=24):
                print(f"[스킵] Alert #{alert['id']} 24시간 내 중복 알림 방지")
                continue

        print(f"[체크] {alert['origin']} → {alert['destination']} ({alert['departure_date']})")
        price = get_lowest_price(
            alert["origin"],
            alert["destination"],
            alert["departure_date"],
            alert["adults"],
            alert["currency"],
        )

        if price is None:
            print("  가격 조회 실패 또는 결과 없음")
            continue

        print(f"  현재 최저가: {price:,.0f} {alert['currency']} | 목표가: {alert['target_price']:,.0f}")
        if price <= alert["target_price"]:
            print("  목표가 이하입니다. 이메일 알림을 전송합니다.")
            sent = send_alert_email(
                alert["email"],
                alert["origin"],
                alert["destination"],
                alert["departure_date"],
                price,
                alert["target_price"],
                alert["currency"],
            )
            if sent:
                update_last_notified(alert["id"])

    print("가격 확인 완료\n")


def start_scheduler():
    scheduler = BlockingScheduler(timezone="Asia/Seoul")
    scheduler.add_job(check_prices, "interval", hours=CHECK_INTERVAL_HOURS)
    print(f"스케줄러 시작: {CHECK_INTERVAL_HOURS}시간마다 가격 확인")
    print("종료하려면 Ctrl+C")
    check_prices()
    scheduler.start()
