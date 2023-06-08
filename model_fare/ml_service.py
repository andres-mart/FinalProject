import json
import time
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


def get_fare():
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
        
        queue, msg = db.brpop(settings.REDIS_QUEUE)
        json_obj = json.loads(msg.decode())
        
        duration = json_obj["duration"]
        time_input = json_obj["time"]

        predict = model_core.predict({"duration":duration,"time":time_input})
        fare = str(predict)
        value = {"fare":fare}
        db.set(json_obj["id"], json.dumps(value))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":

    print("Launching ML Fare service...")
    get_fare()
