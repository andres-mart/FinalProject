# FINAL PROJECT
>  NYC Taxi Fare and Trip Duration Prediction

## The Business problem

Nowadays, many cities present mobility problems and the population, due to the high economic activities, look for the most effective way to travel in terms of time and cost. The ability to predict taxi fares and durations with high accuracy holds tremendous value for both passengers and taxi service providers. For passengers, it allows for better budgeting and planning, ensuring a smooth and seamless travel experience. On the other hand, taxi service providers can benefit from improved revenue management, more efficient dispatching systems, and enhanced customer satisfaction.

In this case we will use information collected on the services provided by yellow cabs in NYC to generate a model that is able to predict the times and fares based on different variables that depend on the distances between the different neighborhoods of the city, traffic, schedules and different aspects that impact the values to be predicted.

A specific analysis of the data for the month of May 2022 was carried out and can be found at the following address https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-05.parquet


## Technical aspects

To develop this solution you will need to have a proper working environment setup in your machine consisting of:
- Docker.
- docker-compose.
- VS Code or any other IDE of your preference.
- Optional: Linux subsystem for Windows (WSL2).

The technologies involved are:
- Python is the main language for all the EDA analysis performed on the dataset, the training and prediction process. 
- Flask framework for the API.
- HTML for the web UI.
- Redis for the communication between microservices.
- Sk-learn and XGboost for the model training and prediction processes. 

###  Modules
```
├── api
│   ├── templates
│   |   └── index.html # API html template
│   ├── utils
│   |   └── readdata.py # This script will read the data from the zone json file. Intended to be used by the front end script named views.py.
│   ├── zone_source
│   │   └── zones.json # Json containing the zones served by NYC yellow cabs adn their unique zone ID
│   ├── app.py # Flask basic configuration settings for the API
│   ├── Dockerfile # Container info for the API service.
│   ├── middleware.py # This script loops infinitely until it receives a response from thefront end, distributes the inputs to the predictive services, and returns the prediction to the front end.
│   ├── settings.py # Redis basic setting for this container
│   └── views.py # front end script.
|
├── model_duration
│   ├── Dockerfile # Container info for the model duration service
│   ├── ml_service.py # Client inputs preprocessing and inference.
│   ├── model_core.py # Model training script. Intended to serve the ml_service script with the ML algorithm trained and ready for prediction.
│   └── settings.py # Redis basic setting for this container
|
├── model_fare
│   ├── Dockerfile #Container info for the model fare service
│   ├── ml_service.py #Client inputs preprocessing and inference.
│   ├── model_core.py # Model training script. Intended to serve the ml_service script with the ML algorithm trained and ready for prediction.
│   └── settings.py # Redis basic setting for this container
|
├── src
│   ├── config.py
│   └── outliers_detection.py # Script for outliers detection in the preprocessing phase of the EDA.
|
├── test
│   └── test_detect.py # Checks the shape of the dataframe
|
├── docker-compose.yml # docker settings and dependencies for the whole infra
├── EDA.ipynb # Exploratory data analysis notebook.
└── README.md
```
Let's take a quick overview of each module:

- api: It has all the needed code to implement the communication interface between the users and our service. It uses Flask and Redis to queue tasks to be processed by our machine learning model.
    - `api/a`: Setup and launch our Flask api.
    - `api/views.py`: Contains the API endpoints. You must implement the following endpoints:
        - *upload_image*: Displays a frontend in which the user can upload an image and get a prediction from our model.
        - *predict*: POST method which receives an image and sends back the model prediction. This endpoint is useful for integration with other services and platforms given we can access it from any               other programming language.
        - *feedback*: Endpoint used to get feedback from users when the prediction from our model is incorrect.
    - `api/utils.py`: Implements some extra functions used internally by our api.
    - `api/settings.py`: It has all the API settings.
    - `api/templates`: Here we put the .html files used in the frontend.
    - `api/tests`: Test suite.
- model: Implements the logic to get jobs from Redis and process them with our Machine Learning model. When we get the predicted value from our model, we must encode it on Redis again so it can be delivered to the user.
    - `model/ml_service.py`: Runs a thread in which it gets jobs from Redis, processes them with the model, and returns the answers.
    - `model/settings.py`: Settings for our ML model.
    - `model/tests`: Test suite.
- tests: This module contains integration tests so we can properly check our system's behavior is expected and functions as intended.

For a schematic idea of how our system works, please refer to the file `System_architecture_diagram.png` to have a graphical description of the microservices and how the communication is performed.


## Usage and installation instructions

To run the services using compose:

```bash
$ cp .env.original .env
```

```bash
$ docker-compose up --build -d
```

To stop the services:

```bash
$ docker-compose down
```

## Code Style

Following a style guide keeps the code's aesthetics clean and improves readability, making contributions and code reviews easier. Automated Python code formatters make sure your codebase stays in a consistent style without any manual work on your end. If adhering to a specific style of coding is important to you, employing an automated to do that job is the obvious thing to do. This avoids bike-shedding on nitpicks during code reviews, saving you an enormous amount of time overall.

We use [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/) for automated code formatting in this project, you can run it with:

```console
$ isort --profile=black . && black --line-length 88 .
```

Wanna read more about Python code style and good practices? Please see:
- [The Hitchhiker’s Guide to Python: Code Style](https://docs.python-guide.org/writing/style/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Tests

We provide unit tests along with the project that you can run and check from your side the code meets the minimum requirements of correctness needed to approve. To run just execute:

### 1. Modules

We make use of [multi-stage docker builds](https://docs.docker.com/develop/develop-images/multistage-build/) so we can have into the same Dockerfile environments for testing and also for deploying our service.

#### 1.1. Test functions

Run:

```bash
$ cd FinalProject/
$ docker build -t flask_test_detect.py --progress=plain --target test .
