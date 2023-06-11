FROM python:3.8.13 as base

ADD model/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./model /src/
ADD ./dataset /src/

WORKDIR /src

#FROM base as test
#RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["python3", "ml_service.py"]

