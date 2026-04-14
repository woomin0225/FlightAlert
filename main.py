import sys

from amadeus_client import test_connection
from db import add_alert, deactivate_alert, init_db, list_alerts


def cmd_add():
    print("=== 새 알림 추가 ===")
    email = input("이메일 주소: ").strip()
    origin = input("출발지 IATA 코드 (예: ICN): ").strip().upper()
    destination = input("도착지 IATA 코드 (예: LAX): ").strip().upper()
    departure_date = input("출발 날짜 (YYYY-MM-DD): ").strip()
    target_price = float(input("목표 가격 (KRW): ").strip())

    add_alert(email, origin, destination, departure_date, target_price)
    print(f"알림 추가 완료: {origin} → {destination} / {departure_date} / 목표가 {target_price:,.0f}원")


def cmd_list():
    alerts = list_alerts()
    if not alerts:
        print("등록된 알림이 없습니다.")
        return

    print(f"\n{'ID':<4} {'이메일':<28} {'노선':<14} {'출발일':<12} {'목표가':>12} {'상태'}")
    print("-" * 86)
    for alert in alerts:
        route = f"{alert['origin']}→{alert['destination']}"
        status = "활성" if alert["active"] else "비활성"
        print(f"{alert['id']:<4} {alert['email']:<28} {route:<14} {alert['departure_date']:<12} {alert['target_price']:>12,.0f} {status}")
    print()


def cmd_delete():
    cmd_list()
    alert_id = int(input("비활성화할 알림 ID: ").strip())
    deactivate_alert(alert_id)
    print("알림을 비활성화했습니다.")


def cmd_test():
    ok = test_connection()
    print("Amadeus 연결 성공" if ok else "Amadeus 연결 실패")


def print_help():
    print(
        """
사용법: python main.py [명령]

  add     새 알림 추가
  list    알림 목록 확인
  delete  알림 비활성화
  test    Amadeus 연결 테스트
  run     스케줄러 시작
"""
    )


if __name__ == "__main__":
    init_db()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""

    if cmd == "add":
        cmd_add()
    elif cmd == "list":
        cmd_list()
    elif cmd == "delete":
        cmd_delete()
    elif cmd == "test":
        cmd_test()
    elif cmd == "run":
        from scheduler import start_scheduler

        start_scheduler()
    else:
        print_help()
