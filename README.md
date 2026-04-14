# FlightAlert

FlightAlert는 항공권 가격 변화를 간단하게 확인하고 알림까지 관리할 수 있는 Windows 데스크톱 앱입니다.  
UI는 `customtkinter` 기반이며, 기본적으로는 mock 데이터를 사용하고 필요할 때 Amadeus API와 이메일 알림을 연결할 수 있습니다.

## 주요 기능

- 대시보드에서 노선별 가격 흐름 확인
- 출발편, 귀국편, 총액을 분리해서 비교
- 보고서 페이지와 가격 시각화 제공
- UI에서 가격 알림 생성 및 관리
- 라이트/다크 테마 전환
- Windows 시작 시 자동 실행 옵션 지원

## 실행 방법

### 소스코드로 실행

```powershell
pip install -r requirements.txt
python app.py
```

### CLI 도구 실행

```powershell
python main.py
```

또는:

```powershell
python -m backend.cli
```

지원 명령:

- `add`
- `list`
- `delete`
- `test`
- `run`

## 프로젝트 구조

```text
app.py                     # 데스크톱 UI 실행 진입점
main.py                    # CLI 실행 진입점
flightalert/               # 실제 UI 코드
backend/                   # 알림/DB/API/스케줄러 코드
README.md
requirements.txt
```

## 환경 변수

실시간 API 또는 이메일 알림을 사용하려면 `.env` 파일을 설정하면 됩니다.

```env
AMADEUS_CLIENT_ID=your_client_id
AMADEUS_CLIENT_SECRET=your_client_secret
AMADEUS_HOSTNAME=test

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

CHECK_INTERVAL_HOURS=6
```

## 기술 스택

- Python
- customtkinter
- matplotlib
- numpy
- sqlite3
- Amadeus Python SDK

## 배포 메모

- `.env`, `alerts.db`, `routes_data.json`, `dist/`, `build/`는 버전 관리에서 제외됩니다.
- API 자격 증명이 없으면 앱은 mock 데이터 기반으로 동작합니다.
- 자동 실행 옵션은 앱 설정에서 켜고 끌 수 있습니다.
