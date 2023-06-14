import os
from pathlib import Path

# REDIS
# Queue name
REDIS_QUEUE = "service"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = os.getenv("REDIS_IP", "redis")
# Sleep parameters which manages the
# interval between requests to our redis queue
SERVER_SLEEP = 0.05

GOOGLE_API_KEY="AIzaSyCP-1qFF-vI7fGe0H7QiJDCgZuGehYfcBE"

DATASET_ROOT_PATH = str(Path(__file__).parent.parent / "dataset")
os.makedirs(DATASET_ROOT_PATH, exist_ok=True)

