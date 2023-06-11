import pandas as pd
import geopy.distance

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

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

    #Estimate trip distance using lat and long
    lat1 = data[data["PULocationID"].isin([start_point])].PULat.mean()
    lon1 = data[data["PULocationID"].isin([start_point])].PULong.mean()
    lat2 = data[data["DOLocationID"].isin([dest_point])].DOLat.mean()
    lon2 = data[data["DOLocationID"].isin([dest_point])].DOLong.mean()
            
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    trip_distance = geopy.distance.geodesic(coords_1, coords_2).km

    #Estimate median speed at that given time
    speed_minutes = data[data["hour_pickup"] == hour_input]["speed_minutes"].median()

    train_df, test_df = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)

    X_train = train_df[["trip_distance", "speed_minutes"]]
    y_train = train_df["fare_amount"]

    #scaler = MinMaxScaler()
    #scaler = scaler.fit(X_train)

    inputs_fare = {"trip_distance" : trip_distance, "speed_minutes": speed_minutes}
    #inputs_to_predict_fare = pd.DataFrame([inputs_fare])
    #inputs_fare_scaled = scaler.transform(inputs_to_predict_fare)

    #Scale values
    xgreg = XGBRegressor()
    xgreg.fit(X_train, y_train)

    #predict_fare = xgreg.predict(inputs_fare_scaled)
    predict_fare = xgreg.predict(inputs_fare)
    
    fare = str(predict_fare)

    ##########################################################################################
    #Get duration

    X_train = train_df[["trip_distance", "speed_minutes","fare_amount"]]
    y_train = train_df["duration"]

    #scaler = MinMaxScaler()
    #scaler = scaler.fit(X_train)

    inputs_duration = {"trip_distance" : trip_distance, "speed_minutes": speed_minutes, "fare_amount":predict_fare}
    #inputs_to_predict_duration = pd.DataFrame([inputs_duration])
    #inputs_duration_scaled = scaler.transform(inputs_to_predict_duration)

    xgreg.fit(X_train, y_train)

    #predict_duration = xgreg.predict(inputs_duration_scaled)
    predict_duration = xgreg.predict(inputs_duration)
    
    duration = str(predict_duration)

    prediction_value = {"duration":duration,"fare": fare}

    return prediction_value