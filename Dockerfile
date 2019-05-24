FROM ubuntu:16.04

WORKDIR /test

COPY . /test

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y install python-pip python-dev curl pylint
RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["pylint", "./main.py"]

