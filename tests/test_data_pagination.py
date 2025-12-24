import requests

BASE_URL = "http://localhost:8000"

def test_data_pagination_limit():
    r = requests.get(f"{BASE_URL}/data?limit=5")
    assert r.status_code == 200
    body = r.json()
    assert "data" in body
    assert len(body["data"]) <= 5

