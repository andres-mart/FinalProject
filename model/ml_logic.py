import pandas as pd
import geopy.distance
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
import googlemaps
import requests



api_key = "google maps api key"

start_point = None
dest_point = None
time_input = None
hour_input = None
duration = None
fare = None

def predict(data,start_point,dest_point,hour_input):
    """
    Predict data based on start point and destination point 
    in a specific hour of the day
    """

    # #Estimate trip distance using lat and long
    gmaps = googlemaps.Client(key=api_key)
    origin = start_point
    destination = dest_point

    traffic_result = gmaps.directions(origin=origin, destination=destination, mode="driving", departure_time="now", units="metric")
    if traffic_result:
        duration_in_traffic = traffic_result[0]['legs'][0]['duration_in_traffic']['value']
        duration_in_minutes = duration_in_traffic / 60
        trip_distance = traffic_result[0]['legs'][0]['distance']['value']
        trip_distance = trip_distance / 1000
        speed_minutes = trip_distance/duration_in_minutes
    else:
        print("Zone not found, please try with nearest zone.")

    url = "https://apis.tollguru.com/toll/v2/origin-destination-waypoints"
    
    new_origin = origin + ", NY 10007 USA"
    new_dest = destination + ", NY 10007 USA"
    payload = {
        "from": {"address": new_origin},
        "to": {"address": new_dest},
        "serviceProvider": "here",
        "vehicle": {
            "type": "2AxlesAuto",
            "weight": {
                "value": 20000,
                "unit": "pound"
            },
            "height": {
                "value": 7.5,
                "unit": "meter"
            },
            "length": {
                "value": 7.5,
                "unit": "meter"
            },
            "axles": 4,
            "emissionClass": "euro_5"
        }
    }
    headers = {
        "content-type": "application/json",
        "x-api-key": "toll guru api key"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data_tolls = response.json()

    toll_cost = data_tolls['routes'][0]['costs']['minimumTollCost']
    ##########################################################################################
    train_df, test_df = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)
    X_train = train_df[["trip_distance", "speed_minutes", "duration", "tolls_amount"]]
    y_train = train_df["fare_amount"]

    scaler = MinMaxScaler()
    scaler = scaler.fit(X_train)

    #inputs_fare = {"trip_distance" : trip_distance, "speed_minutes": speed_minutes}

    input_data = pd.DataFrame([[trip_distance, speed_minutes, duration_in_minutes, toll_cost]],columns=["trip_distance", "speed_minutes", "duration","tolls_amount"])

    #inputs_to_predict_fare = pd.DataFrame([inputs_fare])
    inputs_fare_scaled = scaler.transform(input_data)

    #Scale values
    xgreg = XGBRegressor()
    xgreg.fit(X_train, y_train)

    #predict_fare = xgreg.predict(inputs_fare_scaled)
    predict_fare = xgreg.predict(inputs_fare_scaled)
    
    fare = str(predict_fare)
    ##########################################################################################
    #Get duration

    X_train = train_df[["trip_distance", "speed_minutes","fare_amount"]]
    y_train = train_df["duration"]

    #scaler = MinMaxScaler()
    #scaler = scaler.fit(X_train)

    #inputs_duration = {"trip_distance" : trip_distance, "speed_minutes": speed_minutes, "fare_amount":predict_fare}
    #inputs_to_predict_duration = pd.DataFrame([inputs_duration])
    #inputs_duration_scaled = scaler.transform(inputs_to_predict_duration)
    input_data_duration = pd.DataFrame(np.hstack((np.array([trip_distance]).reshape(-1, 1), np.array([speed_minutes]).reshape(-1, 1), np.array([predict_fare]).reshape(-1, 1))),
        columns=["trip_distance", "speed_minutes", "fare_amount"],
    )

    xgreg.fit(X_train, y_train)

    #predict_duration = xgreg.predict(inputs_duration_scaled)
    predict_duration = xgreg.predict(input_data_duration)
    
    duration = str(predict_duration)

    prediction_value = {"duration":duration,"fare": fare}

    return prediction_value
