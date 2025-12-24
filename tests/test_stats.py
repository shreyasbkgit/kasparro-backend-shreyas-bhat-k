import requests

BASE_URL = "http://localhost:8000"

def test_stats_shape():
    r = requests.get(f"{BASE_URL}/stats")
    assert r.status_code == 200

    body = r.json()
    assert "total_runs" in body
    assert "runs" in body
    assert isinstance(body["runs"], list)

