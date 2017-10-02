FROM node:8.1

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing GUI of an severless app"

# EXPOSE HTTP PORT
EXPOSE 8000

# CREATE AND SET DIRECTORIES
RUN mkdir -p /srvrlss/gui
RUN mkdir -p /srvrlss/gui/app
WORKDIR /srvrlss/gui

# COPY SOURCE CODE FOR SRVLRSS
COPY ./.bowerrc .
COPY ./.jshintrc .
COPY ./bower.json .
COPY ./karma.conf.js .
COPY ./package.json .
VOLUME ["/srvrlss/gui/app"]

# INSTALL SRVRLSS API
RUN npm install

# DEFINE ENTRYPOINT AS GUI
ENTRYPOINT ["npm", "start"]