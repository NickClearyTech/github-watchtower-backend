FROM python:3.10.2-slim-buster

RUN apt-get update && apt-get upgrade -y

WORKDIR /watchtower

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# create an unprivledged user
RUN adduser --disabled-password --gecos '' app

COPY ./app/requirements.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
RUN mkdir /watchtower/app

COPY ./app /watchtower/app
WORKDIR /watchtower/app/watchtower