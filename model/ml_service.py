import json
import time
import redis
import settings
import pandas as pd
import geopy.distance

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from preprocessing import preprocessing
from xgboost import XGBRegressor

db = redis.Redis(host=settings.REDIS_IP,port=settings.REDIS_PORT,db=0)

def get_prediction():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """

    #Processing    

    duration = None
    fare = None

    data = preprocessing()

    while True:

        queue, msg = db.brpop(settings.REDIS_QUEUE)
        json_obj = json.loads(msg.decode())

        start_point = json_obj["start_point"]
        dest_point = json_obj["dest_point"]
        time_input = json_obj["time"]
     
        train_df, test_df = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)

        X_train = train_df[["trip_distance", "speed_minutes"]]
        X_test = test_df[["trip_distance", "speed_minutes"]]
        y_train = train_df["duration"]
        y_test = test_df["duration"]

        scaler = MinMaxScaler()
        scaler = scaler.fit(X_train)

        X_train = pd.DataFrame(scaler.transform(X_train))
        X_test = pd.DataFrame(scaler.transform(X_test))

        #lat1 = data[data["PUZone"].isin([start_point])]
        #lon1 = data[data["PUZone"].isin([start_point])]
        #lat2 = data[data["DOZone"].isin([dest_point])]
        #lon2 = data[data["DOZone"].isin([dest_point])]

        print("Start point") 
        print(start_point) 
        
        print("PULocationID type")
        print(type(data["PULocationID"]))
        print("start_point type")
        print(type(start_point))

        lat1 = data[data["PULocationID"] == start_point].PULat.mean()
        lon1 = data[data["PULocationID"] == start_point].PULong.mean()
        lat2 = data[data["DOLocationID"] == dest_point].DOLat.mean()
        lon2 = data[data["DOLocationID"] == dest_point].DOLong.mean()

        print(lat1)
        print(lon1)
        print(lat2)
        print(lon2)        

        #Estimate trip distance using lat and long
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        trip_distance = geopy.distance.geodesic(coords_1, coords_2).km

        #Estimate median speed at that given time
        speed_minutes = data[data["hour_pickup"] == time_input]["speed_minutes"].median()

        #Scaling inputs
        trip_distance_scaled = scaler.transform(trip_distance)
        speed_minutes_scaled = scaler.transform(speed_minutes)

        xgreg = XGBRegressor()
        xgreg.fit(X_train, y_train)

        predict = xgreg.predict(trip_distance_scaled,speed_minutes_scaled)
        
        duration = str(predict)

        #Get fare




        value = {"duration":duration,"fare": fare}
        db.set(json_obj["id"], json.dumps(value))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":

    print("Launching ML service...")
    get_prediction()
