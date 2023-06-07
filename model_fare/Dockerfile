FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

RUN mkdir -p /src/
ADD ./ /src/
WORKDIR /src

COPY src/config.py /src/
COPY src/preprocessing.py /src/
COPY dataset/taxi+_zone_lookup.csv /src/
COPY dataset/yellow_tripdata_2022-05.parquet /src/
COPY dataset/taxi_zone_lookup_coordinates.csv /src/

#FROM base as test
#RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["python3", "ml_service.py"]

