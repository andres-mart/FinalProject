import json
import os
import time

import numpy as np
import redis
import settings
import model_core

db = redis.Redis(host=settings.REDIS_IP,port=settings.REDIS_PORT,db=0)

def predict(request):

    """
    Get parameters of the ride and then, run our ML model to get predictions.

    Parameters
    ----------
    ride_request : dictionary
        point_from: 
        point_to:
        time: 

    Returns
    ------- 
    class_name, pred_probability : tuple(str, float)
        Model predicted the fair of ride and other data
    """

    return model_core.predict(request)


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """

    while True:
        print("classify_process")
        queue, msg = db.brpop(settings.REDIS_QUEUE)
        json_obj = json.loads(msg.decode())

        point_from = json_obj["point_from"]
        point_to = json_obj["point_to"]
        time = json_obj["time"]

        p = predict({"point_from":point_from,"point_to":point_to,"time":time})
        fair = str(p[0])
        time = str(p[1])
        value = {"fair":fair, "time":time}
        db.set(json_obj["id"], json.dumps(value))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()
