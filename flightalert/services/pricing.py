import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..mock_data import build_route_mock_data

try:
    from amadeus import Client, ResponseError
except Exception:  # pragma: no cover - optional dependency at runtime
    Client = None
    ResponseError = Exception


@dataclass
class PriceSnapshot:
    current_price: float
    currency: str
    source: str
    provider: str
    is_live: bool
    message: str = ""
    outbound_price: Optional[float] = None
    inbound_price: Optional[float] = None


class PricingService:
    def __init__(self):
        self._client = None
        self._cache_key = None

    def get_snapshot(self, route, settings=None, prefer_live=False):
        settings = settings or {}
        if prefer_live:
            live = self._fetch_live_snapshot(route, settings)
            if live is not None:
                return live
        return self._build_mock_snapshot(route)

    def test_connection(self, settings=None):
        settings = settings or {}
        client = self._get_client(settings)
        if client is None:
            return False, "Amadeus 라이브러리 또는 API 자격증명이 없습니다."
        try:
            client.reference_data.locations.get(keyword="ICN", subType="AIRPORT")
            return True, "Amadeus 테스트 환경 연결에 성공했습니다."
        except ResponseError as exc:
            return False, f"Amadeus 응답 오류: {exc}"
        except Exception as exc:
            return False, f"연결 테스트 실패: {exc}"

    def _fetch_live_snapshot(self, route, settings):
        client = self._get_client(settings)
        if client is None:
            return None

        segments = route.get("segments", [])
        if not segments:
            return None

        try:
            outbound_price = self._fetch_segment_price(client, segments[0], route)
            if outbound_price is None:
                return None

            inbound_price = None
            if len(segments) > 1:
                inbound_price = self._fetch_segment_price(client, segments[-1], route)
                if inbound_price is None:
                    return None

            total_price = outbound_price + (inbound_price or 0.0)
            return PriceSnapshot(
                current_price=total_price,
                currency="KRW",
                source="live",
                provider="Amadeus",
                is_live=True,
                message=f"실시간 Amadeus 조회 · {datetime.now().strftime('%H:%M')}",
                outbound_price=outbound_price,
                inbound_price=inbound_price,
            )
        except ResponseError:
            return None
        except Exception:
            return None

    def _fetch_segment_price(self, client, segment, route):
        response = client.shopping.flight_offers_search.get(
            originLocationCode=segment.get("origin", ""),
            destinationLocationCode=segment.get("destination", ""),
            departureDate=segment.get("date", ""),
            adults=max(int(route.get("adults", 1)), 1),
            currencyCode="KRW",
            max=5,
        )
        offers = getattr(response, "data", None) or []
        if not offers:
            return None
        prices = sorted(
            float(offer["price"]["total"])
            for offer in offers
            if offer.get("price", {}).get("total")
        )
        return prices[0] if prices else None

    def _build_mock_snapshot(self, route):
        mock = build_route_mock_data(route)
        outbound_price, inbound_price = self._split_mock_total(route, float(mock["current_price"]))
        return PriceSnapshot(
            current_price=float(mock["current_price"]),
            currency="KRW",
            source="mock",
            provider="Mock",
            is_live=False,
            message="API 연결 전 mock 데이터",
            outbound_price=outbound_price,
            inbound_price=inbound_price,
        )

    def _split_mock_total(self, route, total_price):
        segments = route.get("segments", [])
        if len(segments) <= 1:
            return total_price, None

        # Slightly bias outbound for long-haul departures while keeping deterministic totals.
        ratio = 0.54 if route.get("id", 0) % 2 else 0.57
        outbound = round(total_price * ratio)
        inbound = max(total_price - outbound, 0)
        return float(outbound), float(inbound)

    def _get_client(self, settings):
        if Client is None:
            return None
        client_id = settings.get("amadeus_id") or os.getenv("AMADEUS_CLIENT_ID")
        client_secret = settings.get("amadeus_secret") or os.getenv("AMADEUS_CLIENT_SECRET")
        hostname = settings.get("amadeus_env") or os.getenv("AMADEUS_HOSTNAME") or "test"
        key = (client_id, client_secret, hostname)
        if not client_id or not client_secret:
            return None
        if self._client is None or self._cache_key != key:
            self._client = Client(client_id=client_id, client_secret=client_secret, hostname=hostname)
            self._cache_key = key
        return self._client
