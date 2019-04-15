#!/bin/bash

# Create directories
mkdir -p volumes
mkdir -p volumes/database

# Start docker containers
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  up -d --build --force-recreate
