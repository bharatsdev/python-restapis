FROM python:3.7-alpine

MAINTAINER EveryThingIsData

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache  postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual ./temp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN apk del ./temp-build-deps

RUN mkdir /app

WORKDIR /app

COPY ./app /app

# Crete users for the images, so image will not be deployed in root
RUN adduser -D user
RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static
#
RUN chown -R user:user /vol/
RUN chmod 755 /vol/web

USER user