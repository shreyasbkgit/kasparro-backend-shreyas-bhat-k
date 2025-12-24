import requests

BASE_URL = "http://localhost:8000"

def test_filter_coingecko():
    r = requests.get(f"{BASE_URL}/data?source=coingecko")
    assert r.status_code == 200
    body = r.json()

    for row in body["data"]:
        assert row["source"] == "coingecko"


def test_filter_coinpaprika():
    r = requests.get(f"{BASE_URL}/data?source=coinpaprika")
    assert r.status_code == 200
    body = r.json()

    for row in body["data"]:
        assert row["source"] == "coinpaprika"

