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
│   |   └── index.html 
│   ├── utils
│   |   └── readdata.py 
│   ├── zone_source
│   │   └── PUZonesID.json 
│   │   └── DOZonesID.json
│   ├── app.py 
│   ├── Dockerfile 
│   ├── middleware.py 
│   ├── settings.py 
│   └── views.py 
|
├── model
│   ├── Dockerfile 
│   ├── ml_service.py 
│   ├── model_core.py # Model training script. Intended to serve the ml_service script with the ML algorithm trained and ready for prediction.
│   └── settings.py 
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
Let's take a quick overview of each module:

- api: It has all the needed code to implement the communication interface between the users and our service. It uses Flask and Redis to queue tasks to be processed by our machine learning model.
    - `template/index`: API html template.
    - `utils/readdata.py`: This script will read the data from the zone json file. Intended to be used by the front end script named views.py.
    - `zone_source/PUZoneID.json`: Json containing the zones served by NYC yellow cabs adn their unique zone ID.
    - `zone_source/DOZoneID.json`: Json containing the zones served by NYC yellow cabs adn their unique zone ID.
    - `api/app.py`: Flask basic configuration settings for the API
    - `api/Dockerfile`: Container info for the API service.
    - `api/middleware.py`: his script loops infinitely until it receives a response from thefront end, distributes the inputs to the predictive services, and returns the prediction to the front end.
    - `api/settings.py`: Redis basic setting for this container.
    - `api/views.py`: Front end script.
- model: Implements the logic to get jobs from Redis and process them with our Machine Learning model. When we get the predicted value from our model, we must send it on Redis again so it can be delivered to the user.
    - `model/Dockerfile`: Container info for the model duration and fare service.
    - `model/ml_service.py`: Client inputs preprocessing and inference.
    - `settings.py`: Redis basic setting for this container.
- src: source module for general configuration and functions.
    - `config.py`: Gneral configuration and root path.
    - `outliers_detection.py`: Script for outliers detection in the preprocessing phase of the EDA.
- test: This module contains integration tests so we can properly check our system's behavior is expected and functions as intended.
    - `test_detect.py`: Checks the shape of the dataframe
- General module.
    - `docker-compose.yml`: Docker settings and dependencies for the whole infrastructure.
    - `EDA.ipynb`: Exploratory data analysis notebook.
    
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
