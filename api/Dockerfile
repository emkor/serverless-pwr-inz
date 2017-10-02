FROM srvrlss-executor:latest

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing API functionalities of an severless app"

# ESPOSE HTTP PORT
EXPOSE 8080

# CREATE AND SET DIRECTORIES
RUN mkdir -p /srvrlss/api
WORKDIR /srvrlss/api

# COPY SOURCE CODE FOR SRVLRSS
COPY . .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL SRVRLSS API
RUN pip install .

# DEFINE ENTRYPOINT AS COORDINATOR API
ENTRYPOINT ["python", "./app.py"]