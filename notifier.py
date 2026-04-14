import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER


def send_alert_email(to_email, origin, destination, departure_date, current_price, target_price, currency):
    subject = f"항공권 가격 알림: {origin} → {destination} {departure_date}"
    body = f"""안녕하세요.

설정하신 가격 알림 조건이 충족되었습니다.

- 노선: {origin} → {destination}
- 출발일: {departure_date}
- 현재 최저가: {current_price:,.0f} {currency}
- 목표 가격: {target_price:,.0f} {currency}

지금 바로 예약 가능 여부를 확인해 보세요.

이 알림은 FlightAlert에서 자동 발송되었습니다.
"""

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER or ""
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[이메일] 발송 완료: {to_email}")
        return True
    except Exception as exc:
        print(f"[이메일] 발송 실패: {exc}")
        return False
