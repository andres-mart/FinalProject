import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

from src import preprocessing as prep

def predict(request):

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

    filtered_df = prep.preprocessing()

    train_df, test_df = train_test_split(filtered_df, test_size=0.2, random_state=42, shuffle=True)

    X_train = train_df.drop("duration", axis=1)
    X_test = test_df.drop("duration", axis=1)
    y_train = train_df["duration"]
    y_test = test_df["duration"]

    columns = X_train.columns
    scaler = MinMaxScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns= columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns= columns)

    xgreg = XGBRegressor()
    xgreg.fit(X_train, y_train)
    predict = xgreg.predict(X_test)

    return predict[0]