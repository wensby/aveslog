#!/bin/bash

docker-compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  up -d --no-deps --build \
  birding-web-service
