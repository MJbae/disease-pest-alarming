FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3-pip libcurl4-openssl-dev libssl-dev default-libmysqlclient-dev build-essential && apt-get clean

ENV PYTHONUNBUFFERED=1

WORKDIR /code
ADD .. /code

RUN pip3 install --upgrade --ignore-installed pip setuptools && pip3 install -r requirements.txt