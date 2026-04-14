# FlightAlert

FlightAlert는 항공권 가격 변화를 간단하게 확인하고 알림까지 관리할 수 있는 Windows 데스크톱 앱입니다.

## 가장 쉬운 실행 방법

1. 이 저장소에서 `release/FlightAlert_Portable_v2.exe` 파일을 다운로드합니다.
2. 파일을 더블클릭해서 바로 실행합니다.

추가 설치 없이 실행할 수 있도록 만든 휴대용 버전입니다.

## 소스코드 실행 방법

```powershell
pip install -r requirements.txt
python app.py
```

## CLI 도구 실행

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

## 주요 기능

- 대시보드에서 노선별 가격 흐름 확인
- 출발편, 귀국편, 총액을 분리해서 비교
- 보고서 페이지와 가격 시각화 제공
- UI에서 가격 알림 생성 및 관리
- 라이트/다크 테마 전환
- Windows 시작 시 자동 실행 옵션 지원

## 프로젝트 구조

```text
app.py                     # 데스크톱 UI 실행 진입점
main.py                    # CLI 실행 진입점
flightalert/               # 실제 UI 코드
backend/                   # 알림/DB/API/스케줄러 코드
release/                   # 배포용 실행 파일
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
- GitHub에서 바로 받을 수 있는 실행 파일은 `release/FlightAlert_Portable_v2.exe`에 포함됩니다.
- API 자격 증명이 없으면 앱은 mock 데이터 기반으로 동작합니다.
