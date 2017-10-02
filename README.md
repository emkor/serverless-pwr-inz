# Serverless-based project
Mateusz Korzeniowski's Engineering Thesis in Computer Science for Wrocław University of Science and Technology: *Web based application supporting planning of tourist travel, built using Serverless architectural pattern*

# What is it about?
The thesis focuses mostly on comparison between using distributed approach (using Celery framework) and serverless approach (AWS Lambda) as computational backend to retrieve and parse data from external services (Instagram, SkyScanner, OpenWeather, Uber APIs) and show particular info about potential travel between two European cities.

Available info includes: costs of Flights, Uber pricing, weather forecasts and Instagram real-time photos of the destination place.

# Usage
Requirements:
- Linux distro (I haven't tested it on Windows but I think it should run just fine)
- Docker and docker-compose installed
- Serverless framework installed

App can be launched in one of two modes: see USE_AWS_LAMBDA switch in docker-compose.yml file. Also, please make sure you have valid access keys to external services (docker-compose.yml file and serverless.yml need to be configured with them) so the app will be allowed to use external APIs.

To build the images and start the app, please use bash script **docker-build-images.sh** and then **docker-compose up** command. App web UI is available on 8000 port on localhost.

To run with AWS Lambda backend, you need to also package and upload code from srvrlss directory using Serverless framework tool (see serverless.yml file).

# Technical details
App consists of three main components: GUI (angularjs), Local API (Python, CherryPy) and Executor (either Python and Celery or Python and AWS Lambda). Each component runs in Docker container.

Requests from UI are being passed to Local API (dispatcher-thing) that either:
 - sends tasks to RabbitMQ broker, which then sends them to Celery workers)
 - makes calls to AWS Lambda HTTP API that triggers functions on their servers.
  
Then results are bing returned by Local API and shown in Web UI.

# Screens

App Desktop UI:

![App Desktop UI](https://github.com/emkor/serverless-pwr-inz/raw/master/praca-inz/img/app_ui1.png "App Desktop UI")

***

App Mobile UI:

![App Mobile UI](https://github.com/emkor/serverless-pwr-inz/raw/master/praca-inz/img/app_ui2.png "App Mobile UI")
