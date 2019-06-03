FROM ubuntu:16.04

WORKDIR /CS230-Term-Project

COPY . /CS230-Term-Project

ENV DEBIAN_FRONTEND noninteractive

RUN apt -y update
RUN apt -y install vim git python3 python-pip python-dev curl python3-pip
RUN pip install -U pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip3 install --upgrade pandas google-api-python-client google-auth-httplib2 google-auth-oauthlib


CMD ["python", "./main.py"]

