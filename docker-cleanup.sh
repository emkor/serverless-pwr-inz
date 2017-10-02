#!/usr/bin/env bash
docker ps -a | grep "serverless" | awk '{print $1}' | xargs docker stop || true
docker ps -a | grep "serverless" | awk '{print $1}' | xargs docker rm || true
docker images | grep "srvrlss" | awk '{print $1}' | xargs docker rmi || true