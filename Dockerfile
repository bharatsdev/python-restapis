FROM python:3.7-alpine

MAINTAINER EveryThingIsData

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app

WORKDIR /app

COPY ./app /app

# Crete user for the images, so image will not be deployed in root
RUN adduser -D user
USER user