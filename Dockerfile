FROM ubuntu:16.04
MAINTAINER Eashver Elango <eashvere@gmail.com>

RUN mkdir /code
WORKDIR /code
ADD . /code/
ADD etc /etc

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUn apt-get update
RUN apt-get -y install python3.6

RUN python3 -V

RUN apt-get update && apt-get install -y  \
        openmpi-bin \
        python3-venv \
        python3-tk \
        sqlite3 \
        python3-dev \
        python3-setuptools \
        build-essential \
        python3-wheel \
        libssl-dev \
        libffi-dev \
        python3-pip \
        supervisor \
        nginx && \
    rm /etc/nginx/sites-enabled/default && \
    cp /code/nginx/app /etc/nginx/sites-available/ && \
    ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/

RUN pip3 install --upgrade pip

RUN pip3 install -r /code/requirements.txt

RUN apt update && apt install -y libsm6 libxext6 libxrender-dev libgtk2.0-dev

EXPOSE 88
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
