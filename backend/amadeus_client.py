try:
    from amadeus import Client, ResponseError
except Exception:  # pragma: no cover - optional runtime dependency
    Client = None
    ResponseError = Exception

from .config import AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, AMADEUS_HOSTNAME

_client = None
_client_key = None


def get_client():
    global _client, _client_key
    if Client is None:
        raise RuntimeError("amadeus 패키지가 설치되어 있지 않습니다.")

    client_id = AMADEUS_CLIENT_ID
    client_secret = AMADEUS_CLIENT_SECRET
    hostname = AMADEUS_HOSTNAME or "test"
    if not client_id or not client_secret:
        raise RuntimeError("Amadeus API 자격증명이 설정되지 않았습니다.")

    key = (client_id, client_secret, hostname)
    if _client is None or _client_key != key:
        _client = Client(client_id=client_id, client_secret=client_secret, hostname=hostname)
        _client_key = key
    return _client


def get_lowest_price(origin, destination, departure_date, adults=1, currency="KRW"):
    try:
        client = get_client()
        response = client.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=max(int(adults), 1),
            currencyCode=currency,
            max=5,
        )
        offers = response.data or []
        if not offers:
            return None
        prices = [float(offer["price"]["total"]) for offer in offers if offer.get("price", {}).get("total")]
        return min(prices) if prices else None
    except ResponseError as exc:
        print(f"[Amadeus] API 오류: {exc}")
        return None
    except Exception as exc:
        print(f"[Amadeus] 예외 발생: {exc}")
        return None


def test_connection():
    try:
        client = get_client()
        client.reference_data.locations.get(keyword="ICN", subType="AIRPORT")
        return True
    except Exception as exc:
        print(f"[Amadeus] 연결 테스트 실패: {exc}")
        return False
