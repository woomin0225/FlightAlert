# FlightAlert Working Notes

## 프로젝트 목적

FlightAlert는 Windows에서 실행되는 항공권 가격 모니터링 데스크톱 앱이다.  
핵심 방향은 다음과 같다.

- 심플한 디자인
- 심플한 기능
- 작은 화면에서도 한눈에 보기 쉬운 정보 배치
- mock 데이터 기반 기본 동작
- 필요 시 API 및 이메일 알림 연결
- 하드코딩보다 재사용 가능한 구조 우선

## 현재 구조

루트에는 진입점과 문서만 남기고, 실제 코드는 기능별 폴더로 정리했다.

```text
app.py                     # 데스크톱 UI 실행 진입점
main.py                    # CLI 실행 진입점
flightalert/               # 실제 UI 코드
backend/                   # DB / 알림 / API / 스케줄러
release/                   # 배포용 exe
README.md
CLAUDE.md
```

### UI 코드

- `flightalert/app.py`: 앱 실행과 메인 UI 조립
- `flightalert/pages/`: 페이지별 UI
- `flightalert/widgets.py`: 공통 위젯
- `flightalert/ui_helpers.py`: 차트, 타임라인 등 보조 UI 로직
- `flightalert/theme.py`: 라이트/다크 테마 팔레트
- `flightalert/services/`: UI가 사용하는 서비스 계층

### 백엔드 코드

- `backend/db.py`: 알림 DB
- `backend/amadeus_client.py`: Amadeus API 연동
- `backend/notifier.py`: 이메일 알림
- `backend/scheduler.py`: 백그라운드 체크
- `backend/cli.py`: CLI 명령 진입점

## 최근 반영 사항

- 루트에 흩어져 있던 백엔드 파일을 `backend/` 패키지로 이동했다.
- `main.py`는 이제 `backend.cli`를 호출하는 얇은 런처다.
- `flightalert/services/alerts.py`는 `backend.db`를 참조하도록 변경했다.
- GitHub 공개 저장소 기준으로 구조를 정리했다.
- 실행 파일을 저장소의 `release/FlightAlert_Portable_v2.exe`로 배포 가능하게 올렸다.
- README는 `exe 다운로드 후 실행`을 가장 쉬운 실행 방법으로 안내하도록 맞췄다.

## 실행 규칙

### UI 실행

```powershell
python app.py
```

### CLI 실행

```powershell
python main.py
```

또는:

```powershell
python -m backend.cli
```

## 배포 규칙

- 다른 사람에게는 가능하면 소스코드보다 `release/FlightAlert_Portable_v2.exe` 다운로드 실행을 안내한다.
- GitHub 저장소에서 바로 받을 수 있도록 `release/` 폴더에 exe를 둔다.
- 현재 exe는 약 81MB이므로 GitHub 경고는 있지만 업로드는 가능하다.
- 장기적으로는 GitHub Releases 또는 더 작은 빌드 산출물도 고려할 수 있다.

## 작업 시 주의사항

- 기본 동작은 mock 데이터 유지
- `routes_data.json` 포맷은 바꾸지 않음
- 외부 패키지는 `customtkinter`, `matplotlib`, `numpy`, `tkinter` 범위 중심 유지
- UI는 정보량을 줄이고 작은 노트북 화면에 맞게 계속 최적화
- 박스 크기, 여백, 정보 밀도는 계속 줄이는 방향 선호
- 대시보드에는 불필요한 정보보다 핵심 비교 정보 우선
- 라이트 모드는 기본값이며, 테마 전환 시 색상 반영 오류가 없도록 확인

## 다음 작업자가 우선 확인할 것

1. `python app.py`가 정상 실행되는지 확인
2. 라이트/다크 테마 전환이 정상인지 확인
3. 작은 화면에서 대시보드 카드와 코스 카드가 과도하게 크지 않은지 확인
4. 배포용 exe가 최신 상태인지 확인
