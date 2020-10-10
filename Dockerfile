FROM python:3.7-alpine
LABEL key="juudgespy@gmail.com"

ENV PYTHONUNBUFFRED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app-api
WORKDIR /app-api
COPY ./app-api /app-api

RUN adduser -D run_user
USER run_user

