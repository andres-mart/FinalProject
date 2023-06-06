import os

# Run API in Debug mode
API_DEBUG = True

# REDIS settings
# Queue name
REDIS_QUEUE_FARE = "service_fare"
REDIS_QUEUE_DURATION = "service_duration"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = os.getenv("REDIS_IP", "redis")
# Sleep parameters which manages the
# interval between requests to our redis queue
API_SLEEP = 0.05