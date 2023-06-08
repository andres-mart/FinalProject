import json
import time
import redis
import settings
import model_core

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from preprocessing import preprocessing
import geopy.distance

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


def get_duration():
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

        start_point = json_obj["start_point"]
        dest_point = json_obj["dest_point"]
        time_input = json_obj["time"]
        #Processing
        data = preprocessing()
        train_df, test_df = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)

        X_train = train_df[["trip_distance", "speed_minutes", "fare_amount"]]
    
        scaler = MinMaxScaler()
        scaler.fit(X_train)

        lat1 = data[data["PUZone"] == start_point].PULat.mean()
        lon1 = data[data["PUZone"] == start_point].PULong.mean()
        lat2 = data[data["DOZone"] == dest_point].DOLat.mean()
        lon2 = data[data["DOZone"] == dest_point].DOLong.mean()
        #Estimate trip distance using lat and long
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        trip_distance = geopy.distance.geodesic(coords_1, coords_2).km
        #Estimate median speed at that given time
        speed_minutes = data[data["hour_pickup"] == time_input]["speed_minutes"].median()
        #Scaling inputs
        trip_distance_scaled = scaler.transform(trip_distance)
        speed_minutes_scaled = scaler.transform(speed_minutes)
        fare_amount_scaled = scaler.transform()
        #Prediction
        predict = model_core.predict({"trip_distance":trip_distance_scaled,"speed_minutes":speed_minutes_scaled})
        duration = str(predict)
        value = {"duration":duration}
        db.set(json_obj["id"], json.dumps(value))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":

    print("Launching ML Duration service...")
    get_duration()
