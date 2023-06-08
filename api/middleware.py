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
    
    job_id_duration = str(uuid.uuid4())

    job_data_duration = {
        "id": job_id_duration,
        "start_point": request["start_point"],
        "dest_point": request["dest_point"],
        "time": request["time"]
    }

    db.lpush(
        settings.REDIS_QUEUE_DURATION,
        json.dumps(job_data_duration, default=str)
    )

    # Loop until we received the response from our ML model
    while True:

        #output_fare = db.get(job_id_fare)
        output_duration = db.get(job_id_duration)

        #if output_fare is not None and output_duration is not None:
        if output_duration is not None:

            #output_fare = json.loads(output_fare.decode("utf-8"))
            output_duration = json.loads(output_duration.decode("utf-8"))

            #fare = output_fare["fare"]
            duration = output_duration["duration"]

            #db.delete(job_id_fare)
            db.delete(job_id_duration)

            break
    
    if duration is not None:

        job_id_fare = str(uuid.uuid4())
        
        job_data_fare = {
            "id": job_id_fare,
            "duration" : duration,
            "time": request["time"]
        }

        db.lpush(
            settings.REDIS_QUEUE_FARE,
            json.dumps(job_data_fare, default=str)
        )

        while True:

            output_fare = db.get(job_id_fare)

            if output_fare is not None:

                output_fare = json.loads(output_fare.decode("utf-8"))
                fare = output_fare["fare"]
                db.delete(job_id_fare)

                break

    return fare, duration
