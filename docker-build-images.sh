#!/usr/bin/env bash
docker build -t "srvrlss-commons" ./commons
docker build -t "srvrlss-clients" ./clients
docker build -t "srvrlss-executor" ./executor
docker build -t "srvrlss-api" ./api
docker build -t "srvrlss-gui" ./gui