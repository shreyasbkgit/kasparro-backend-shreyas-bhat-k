import subprocess
import requests
import time

BASE_URL = "http://localhost:8000"

def test_etl_creates_stats_entry():
    before = requests.get(f"{BASE_URL}/stats").json()["total_runs"]

    subprocess.run(
        ["docker", "compose", "exec", "api", "python", "services/run_etl.py"],
        check=True
    )

    time.sleep(1)

    after = requests.get(f"{BASE_URL}/stats").json()["total_runs"]
    assert after > before

