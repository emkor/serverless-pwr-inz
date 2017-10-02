FROM srvrlss-clients:latest

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing executor module of an srvrlss app"

# SET WORKDIR
RUN mkdir -p /srvrlss/executor
WORKDIR /srvrlss/executor


# COPY SOURCE CODE FOR SRVRLSS EXECUTOR
COPY . .

# INSTALL MODULE DEPENDENCIES
RUN pip install -r ./requirements.txt

# INSTALL SRVRLSS EXTRACTOR
RUN pip install .

# DEFINE ENTRYPOINT AS CELERY
ENTRYPOINT ["celery", "-A", "executor", "worker", "--loglevel=info"]