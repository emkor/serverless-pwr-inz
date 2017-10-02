#!/usr/bin/env bash

rm -rf .requirements
rm -rf .serverless
serverless remove
serverless deploy -v