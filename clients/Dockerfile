FROM srvrlss-commons:latest

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing API client functionalities of an severless app"

# CREATE AND SET DIRECTORIES
RUN mkdir -p /srvrlss/clients
WORKDIR /srvrlss/clients

# COPY SOURCE CODE FOR SRVLRSS
COPY . .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL SRVRLSS CLIENTS
RUN pip install .