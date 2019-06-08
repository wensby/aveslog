#!/bin/bash

if [ -z "$1" ]; then
  docker-compose \
    -f docker-compose.yml \
    -f docker-compose.dev.yml \
    up -d --no-deps --build --force-recreate
else
  docker-compose \
    -f docker-compose.yml \
    -f docker-compose.dev.yml \
    up -d --no-deps --build --force-recreate $1
fi
