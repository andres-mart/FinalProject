import pandas as pd
import os
import sys
import pickle

from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.dirname(os.getcwd()))

def preprocessing():

    df = pd.read_parquet("dataset/yellow_tripdata_2022-05.parquet") ##change the path for your own local
    #df.sample(10, random_state=42) #seed of randomness for reproducibility

    df2 = pd.read_csv("dataset/taxi+_zone_lookup.csv") 
    df3 = pd.read_csv("dataset/taxi_zone_lookup_coordinates.csv")

    #Auxiliary datasets creation
    df_pickup = pd.merge(df, df2, left_on= "PULocationID", right_on= "LocationID")
    df_dropoff = pd.merge(df, df2, left_on= "DOLocationID", right_on= "LocationID")

    #Compose of the final working dataset
    df["PUZone"] = df_pickup["Zone"]
    df["DOZone"] = df_dropoff["Zone"]

    #Auxiliary datasets creation
    df_lat_pickup = pd.merge(df, df3, left_on= "PULocationID", right_on= "LocationID")
    df_lat_dropoff = pd.merge(df, df3, left_on= "DOLocationID", right_on= "LocationID")

    #Compose of the final working dataset
    df["PULat"] = df_lat_pickup["latitude"]
    df["PULong"] = df_lat_pickup["longitude"]
    df["DOLat"] = df_lat_dropoff["latitude"]
    df["DOLong"] = df_lat_dropoff["longitude"]

    df_subset = df.sample(10000, random_state=42) #seed of randomness for reproducibility

    df_subset["duration"] = df_subset["tpep_dropoff_datetime"] - df_subset["tpep_pickup_datetime"]
    df_subset["duration"] = df_subset["duration"].dt.total_seconds() / 60

    df_subset["trip_distance"] = df_subset["trip_distance"] * 1.61 ### Convertion rate: 1 mile is about 1.61 kilometers.

    df_subset = df_subset.drop(["VendorID", "payment_type", "RatecodeID"], axis=1)
    df_subset = df_subset.drop(["store_and_fwd_flag"], axis=1)

    filtered_df = df_subset.dropna()

    filtered_df = filtered_df[(filtered_df["passenger_count"] > 0) & (filtered_df["passenger_count"] <= 4 )]
    filtered_df = filtered_df[filtered_df["trip_distance"] > 0]
    filtered_df = filtered_df[filtered_df["trip_distance"] < 50]
    filtered_df = filtered_df[(filtered_df["fare_amount"] < 90) & (filtered_df["fare_amount"] > 0)]
    filtered_df = filtered_df[filtered_df["extra"] < 6]
    filtered_df = filtered_df.drop("mta_tax", axis= 1)
    filtered_df = filtered_df.drop("improvement_surcharge", axis= 1)
    filtered_df = filtered_df[filtered_df["total_amount"] > 0]
    filtered_df = filtered_df[filtered_df["duration"] > 0]
    filtered_df["speed_minutes"] = filtered_df["trip_distance"] / filtered_df["duration"]

    df_congestion = filtered_df[filtered_df["congestion_surcharge"] > 0]
    df_congestion['hour_pickup'] = df_congestion['tpep_pickup_datetime'].dt.hour
    df_congestion['minute_pickup'] = df_congestion['tpep_pickup_datetime'].dt.minute

    filtered_df['hour_pickup'] = filtered_df['tpep_pickup_datetime'].dt.hour
    filtered_df['day_pickup'] = filtered_df['tpep_pickup_datetime'].dt.day

    average_speeds = df_congestion.groupby(['hour_pickup', 'DOZone'])['speed_minutes'].mean()
    worst_hours = average_speeds.sort_values(ascending= True).head(15)
    worst_hours = pd.DataFrame(worst_hours).reset_index()

    filtered_df['peak_hour'] = 0
    # Iterate over each row in filtered_df
    for index, row in filtered_df.iterrows():
        hour_pickup = row['hour_pickup']
        dozone = row['DOZone']
        
        # Check if hour_pickup and dozone exist in worst_hours
        if worst_hours[(worst_hours['hour_pickup'] == hour_pickup) & (worst_hours['DOZone'] == dozone)].shape[0] > 0:
            filtered_df.at[index, 'peak_hour'] = 1
    
    filtered_df = filtered_df.drop(["tpep_pickup_datetime", "tpep_dropoff_datetime"], axis=1)

    # Drop off the conflictive outliers zones
    filtered_df = filtered_df[filtered_df["DOZone"] != "Norwood"]
    filtered_df = filtered_df[filtered_df["DOZone"] != "Highbridge"]
    filtered_df = filtered_df[filtered_df["DOZone"] != "Springfield Gardens North"]
    filtered_df = filtered_df[filtered_df["DOZone"] != "Columbia Street"]

    encoder = LabelEncoder() 
    filtered_df["PUZone"] = encoder.fit_transform(filtered_df[["PUZone"]])

    encoder = LabelEncoder() 
    filtered_df["DOZone"] = encoder.fit_transform(filtered_df[["DOZone"]])

    return filtered_df

if __name__ == "__main__":

    print("Preprocessing service...")
    preprocessing()