FROM python:3.7-alpine
LABEL key="juudgespy@gmail.com"

ENV PYTHONUNBUFFRED 1

COPY ./requirements.txt /requirements.txt
# Instaling temp req for postgresql and save them as tmp-build-deps
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# Delete temp req to keep everhting tidy
RUN apk del .tmp-build-deps 

RUN mkdir /app-api
WORKDIR /app-api
COPY ./app-api /app-api

RUN adduser -D run_user
USER run_user

