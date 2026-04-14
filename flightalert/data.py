import json
import os

from .paths import app_base_dir


AIRPORTS = {
    "ICN": "인천국제공항",
    "GMP": "김포국제공항",
    "PUS": "부산 김해공항",
    "CJU": "제주국제공항",
    "IAD": "워싱턴 덜레스",
    "DCA": "워싱턴 내셔널",
    "ORD": "시카고 오헤어",
    "MDW": "시카고 미드웨이",
    "ATL": "애틀랜타 하츠필드",
    "SLC": "솔트레이크시티",
    "LAX": "로스앤젤레스",
    "JFK": "뉴욕 JFK",
    "EWR": "뉴어크",
    "SFO": "샌프란시스코",
    "SEA": "시애틀 타코마",
    "DFW": "댈러스 포트워스",
    "MIA": "마이애미",
    "DEN": "덴버",
    "LAS": "라스베이거스",
    "BOS": "보스턴 로건",
    "HNL": "호놀룰루",
    "NRT": "도쿄 나리타",
    "HND": "도쿄 하네다",
    "PEK": "베이징 서우두",
    "PVG": "상하이 푸동",
    "HKG": "홍콩",
    "SIN": "싱가포르 창이",
    "BKK": "방콕 수완나품",
    "CDG": "파리 샤를드골",
    "LHR": "런던 히드로",
    "FRA": "프랑크푸르트",
}

BASE_PRICES = {1: 1_920_000, 2: 1_650_000, 3: 1_780_000}
BAG_PRICES = {
    "없음 (기내수하물만)": 0,
    "위탁 1개 (23kg)": 95_000,
    "위탁 2개": 185_000,
}
DOW_FACTORS = [1.03, 0.95, 0.93, 1.01, 1.08, 1.05, 1.06]
ADV_DAYS = [7, 14, 21, 30, 45, 60, 90]
ADV_FACTORS = [1.25, 1.18, 1.12, 1.05, 0.95, 0.92, 0.98]
DOW_KR = ["월", "화", "수", "목", "금", "토", "일"]

PROJECT_ROOT = app_base_dir()
DATA_FILE = os.path.join(PROJECT_ROOT, "routes_data.json")

DEFAULT_DATA = {
    "routes": [
        {
            "id": 1,
            "name": "코스 1 · 인천-워싱턴",
            "trip_type": "왕복",
            "segments": [
                {
                    "origin": "ICN",
                    "destination": "IAD",
                    "date": "2026-05-13",
                    "time_from": "09:00",
                    "time_to": "12:00",
                    "arr_time": "10:35",
                },
                {
                    "origin": "IAD",
                    "destination": "ICN",
                    "date": "2026-05-20",
                    "time_from": "12:00",
                    "time_to": "16:00",
                    "arr_time": "17:30",
                },
            ],
            "adults": 1,
            "baggage": "위탁 1개 (23kg)",
            "favorite": True,
        },
        {
            "id": 2,
            "name": "코스 2 · 인천-시카고",
            "trip_type": "왕복",
            "segments": [
                {
                    "origin": "ICN",
                    "destination": "ORD",
                    "date": "2026-05-13",
                    "time_from": "09:00",
                    "time_to": "13:00",
                    "arr_time": "11:15",
                },
                {
                    "origin": "ORD",
                    "destination": "ICN",
                    "date": "2026-05-20",
                    "time_from": "11:00",
                    "time_to": "14:00",
                    "arr_time": "15:00",
                },
            ],
            "adults": 1,
            "baggage": "위탁 1개 (23kg)",
            "favorite": True,
        },
        {
            "id": 3,
            "name": "코스 3 · 인천-애틀랜타",
            "trip_type": "왕복",
            "segments": [
                {
                    "origin": "ICN",
                    "destination": "ATL",
                    "date": "2026-05-15",
                    "time_from": "15:00",
                    "time_to": "18:00",
                    "arr_time": "17:30",
                },
                {
                    "origin": "ATL",
                    "destination": "ICN",
                    "date": "2026-05-20",
                    "time_from": "10:00",
                    "time_to": "13:00",
                    "arr_time": "12:30",
                },
            ],
            "adults": 1,
            "baggage": "위탁 1개 (23kg)",
            "favorite": True,
        },
    ],
    "settings": {
        "email": "",
        "send_days": ["화", "목"],
        "send_time": "09:00",
        "amadeus_id": "",
        "amadeus_secret": "",
    },
}


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return DEFAULT_DATA


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
