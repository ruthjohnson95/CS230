FROM ubuntu:16.04

WORKDIR /CS230-Term-Project

COPY . /CS230-Term-Project

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y install vim git python3 python-pip python-dev curl pylint python3-pip
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip3 install pandas

CMD ["python", "./main.py"]

