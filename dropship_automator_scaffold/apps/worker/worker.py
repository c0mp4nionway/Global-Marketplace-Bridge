import os, time, json, requests
from dotenv import load_dotenv
from rq import Queue, Connection, Worker
from redis import Redis

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
API_BASE = os.getenv("API_BASE", "http://core_api:8000")

redis = Redis.from_url(REDIS_URL)
q = Queue("jobs", connection=redis)

def import_job(ali_id: str, title: str | None = None):
    payload = {"ali_id": ali_id, "title": title, "attrs": {}}
    r = requests.post(f"{API_BASE}/import", json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def run_worker():
    with Connection(redis):
        worker = Worker(["jobs"])
        worker.work(with_scheduler=True)

if __name__ == "__main__":
    # Run a worker by default
    run_worker()
