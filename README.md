# FINAL PROJECT
>  NYC Taxi Fare and Trip Duration Prediction

## The Business problem

Nowadays, many cities present mobility problems and the population, due to the high economic activities, look for the most effective way to travel in terms of time and cost.

In this case we will use information collected on the services provided by yellow cabs in NYC to generate a model that is able to predict the times and fares based on different variables that depend on the distances between the different neighborhoods of the city, traffic, schedules and different aspects that impact the values to be predicted.

A specific analysis of the data for the month of May 2022 was carried out and can be found at the following address https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-05.parquet



## Technical aspects

To develop this solution you will need to have a proper working environment setup in your machine consisting of:
- Docker
- docker-compose
- VS Code or any other IDE of your preference
- Optional: Linux subsystem for Windows (WSL2)



The technologies involved are:
- Python is the main language for all the EDA analysis performed on the dataset, the training and prediction process. 
- Flask framework for the API
- HTML for the web UI
- Redis for the communication between microservices
- Sk-learn and XGboost for the model preprocessing and prediction processes. 

###  Modules
```
├── api
│   ├── templates
│   |   └── index.html
│   ├── utils
│   |   └── readdata.py
│   ├── zone_source
│   │   └── zones.json
│   ├── app.py
│   ├── Dockerfile
│   ├── middleware.py
│   ├── settings.py
│   └── utils.py
|
├── model_duration
│   ├── Dockerfile
│   ├── ml_service.py
│   ├── model_core.py
│   └── settings.py
|
├── model_fare
│   ├── Dockerfile
│   ├── ml_service.py
│   ├── model_core.py
│   └── settings.py
|
├── src
│   ├── config.py
│   └── outliers_detection.py
|
├── test
│   └── test_detect.py
|
├── docker-compose.yml
├── EDA.ipynb
└── README.md
```
