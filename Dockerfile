FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3-pip libcurl4-openssl-dev libssl-dev default-libmysqlclient-dev build-essential && apt-get clean

WORKDIR /djangoproject
ADD . /djangoproject
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 80

RUN ["chmod", "+x", "/djangoproject/startup.sh"]

CMD ["/djangoproject/startup.sh"]