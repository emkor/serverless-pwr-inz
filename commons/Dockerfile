FROM python:2.7-slim

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing common functionalities of an severless app"

# CREATE AND SET DIRECTORIES
RUN mkdir -p /srvrlss/commons
WORKDIR /srvrlss/commons

# COPY SOURCE CODE FOR AUDIOPYLE
COPY . .

RUN apt-get update
RUN apt-get install -y libmysqlclient-dev gcc

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL SRVRLSS COMMON
RUN pip install .