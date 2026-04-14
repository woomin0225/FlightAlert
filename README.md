# FlightAlert

FlightAlert는 항공권 가격을 간단하게 모니터링할 수 있는 Windows용 데스크톱 앱입니다.  
Python, `customtkinter`, `matplotlib`, `numpy` 기반으로 만들어졌고, 기본적으로는 mock 데이터를 사용하며 필요할 때 Amadeus 실시간 조회를 연결할 수 있습니다.

## 핵심 기능

- 노선별 가격 모니터링 대시보드
- 왕복 기준 `출발편 / 귀국편 / 총액` 분리 표시
- 가격 추이 스파크라인과 보고서 페이지 제공
- UI에서 직접 가격 알림 생성/관리
- 라이트/다크 테마 전환
- Windows 시작 시 자동 실행 옵션
  - 자동 실행 시 최소화 상태로 시작해 성능 영향 최소화

## 실행 방법

### 1. 소스코드로 실행

의존성 설치:

```powershell
pip install -r requirements.txt
```

앱 실행:

```powershell
python app.py
```

### 2. 실행 파일로 실행

배포용 단일 실행 파일(`FlightAlert_Portable_v2.exe`)을 더블클릭하면 바로 실행할 수 있습니다.

## 프로젝트 구조

```text
app.py                     # 런처
flightalert/
  app.py                   # 메인 앱
  theme.py                 # 테마 팔레트
  data.py                  # 기본 데이터 / 저장
  ui_helpers.py            # 차트 / 타임라인 UI 보조 함수
  widgets.py               # 공통 위젯
  pages/                   # 화면별 UI
  services/                # 가격 조회 / 알림 / 자동 실행 서비스
```

## 환경변수

실시간 API 또는 이메일 알림을 쓰려면 `.env` 파일을 만들어 주세요.

예시:

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
- 실시간 API 자격증명이 없으면 앱은 자동으로 mock 데이터로 동작합니다.
- Windows 자동 실행은 설정 페이지에서 켜고 끌 수 있습니다.

## 개발 메모

포터블 실행 파일은 아래 명령으로 생성할 수 있습니다.

```powershell
python -m PyInstaller --onefile --windowed --name FlightAlert_Portable app.py
```
