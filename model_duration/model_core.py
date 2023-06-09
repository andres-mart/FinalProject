import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from preprocessing import preprocessing

def predict(data):

    """
    Get parameters of the ride and then, run our ML model to get predictions.

    Parameters
    ----------
    ride_request : dictionary
        start_point: 
        dest_point:
        time: 

    Returns
    ------- 
    class_name, pred_probability : tuple(str, float)
        Model predicted the fair of ride and other data
    """

    duration = 0

    filename = "model_duration.pickle"
    if os.path.isfile(filename):
        xgreg = pickle.load(open(filename, 'rb'))
    else:

        train_df, test_df = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)

        X_train = train_df[["trip_distance", "speed_minutes", "fare_amount"]]
        X_test = test_df[["trip_distance", "speed_minutes", "fare_amount"]]
        y_train = train_df["duration"]
        y_test = test_df["duration"]

        columns = X_train.columns
        scaler = MinMaxScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train), columns= columns)
        X_test = pd.DataFrame(scaler.transform(X_test), columns= columns)

        xgreg = XGBRegressor()
        xgreg.fit(X_train, y_train)

        pickle.dump(xgreg, open(filename, 'wb'))

    predict = xgreg.predict([1])
    duration = predict[0]

    return duration