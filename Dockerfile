FROM python:3.7-alpine

MAINTAINER EveryThingIsData

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache  postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual ./temp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN mkdir /app

WORKDIR /app

RUN pip install -r /requirements.txt

RUN apk del ./temp-build-deps

ADD ./app /app
COPY ./app /app
RUN mkdir -p /vol/web/media/
RUN mkdir -p /vol/web/static/

# Crete users for the images, so image will not be deployed with  root user
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod 777 /vol/web
USER user