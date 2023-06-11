import json
import time
import uuid
import redis
import settings

db = redis.Redis(host=settings.REDIS_IP,port=settings.REDIS_PORT,db=0)

def model_predict(request):
    """
    Receives an object and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    ride_request : dict
        start_point: 
        dest_point:
        time: 

    Returns
    -------
    fair, time : tuple(float, time)
        Model predicted the fare of ride and other data
    """
    
    fare = None
    duration = None
    
    job_id = str(uuid.uuid4())

    job_data = {
        "id": job_id,
        "start_point": request["start_point"],
        "dest_point": request["dest_point"],
        "time": request["time"]
    }

    db.lpush(
        settings.REDIS_QUEUE,
        json.dumps(job_data, default=str)
    )

    # Loop until we received the response from our ML model
    while True:

        output = db.get(job_id)

        if output is not None:

            output = json.loads(output.decode("utf-8"))

            fare = output["fare"]
            duration = output["duration"]

            db.delete(job_id)

            break

    return fare, duration
