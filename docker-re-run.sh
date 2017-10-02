#!/usr/bin/env bash

docker-compose kill
bash ./docker-cleanup.sh
bash ./docker-build-images.sh
docker-compose up