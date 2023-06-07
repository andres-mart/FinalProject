FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/
COPY /../preprocessing.py /src/
COPY /../taxi+_zone_lookup.csv /src/
COPY /../yellow_tripdata_2022-05.parquet /src/

WORKDIR /src

#FROM base as test
#RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["python3", "ml_service.py"]

