import json
import time
import redis
import settings

import ml_logic 
from preprocessing import preprocessing

db = redis.Redis(host=settings.REDIS_IP,port=settings.REDIS_PORT,db=0)

def get_prediction():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.
    """

    #Processing
    data = preprocessing()

    while True:

        queue, msg = db.brpop(settings.REDIS_QUEUE)
        json_obj = json.loads(msg.decode())

        start_point = int(json_obj["start_point"])
        dest_point = int(json_obj["dest_point"])
        time_input = json_obj["time"]
        hour_input = int(time_input.split(":")[0])

        value = ml_logic.predict(data,start_point,dest_point,hour_input)

        db.set(json_obj["id"], json.dumps(value))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":

    print("Launching ML service...")
    get_prediction()
