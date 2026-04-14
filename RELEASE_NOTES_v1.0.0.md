# FlightAlert v1.0.0

## 주요 기능

- 항공권 가격 모니터링 데스크톱 앱 공개
- 왕복 노선 기준 출발편, 귀국편, 총액 분리 표시
- 대시보드 / 코스 관리 / 가격 알림 / 보고서 / 설정 화면 제공
- mock 데이터 기반 기본 동작
- Amadeus 실시간 조회 연결 지원
- Windows 시작 시 자동 실행 옵션 지원

## 포함 내용

- 라이트 모드 기본 적용
- 노트북 화면 기준 UI 밀도 최적화
- 가격 타임라인 시각화 개선
- 가격 알림 UI 추가
- 공개 저장소용 구조 리팩터링

## 실행 방법

### 소스코드 실행

```powershell
pip install -r requirements.txt
python app.py
```

### 포터블 실행 파일

- `FlightAlert_Portable_v2.exe` 더블클릭

## 참고

- Amadeus API 자격증명이 없으면 mock 데이터로 동작합니다.
- 자동 실행은 설정 페이지에서 켜고 끌 수 있습니다.
