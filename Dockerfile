FROM python:3.8-slim

WORKDIR /mydata

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY flight_prices_training.csv ./flight_prices_training.csv
COPY flight_prices_predict.csv ./flight_prices_predict.csv.

COPY train.py ./train.py
COPY app.py ./app.py

RUN python3 train.py