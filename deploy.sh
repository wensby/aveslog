#!/bin/bash

# Validate prerequisites and arguments
if [ ! -f docker-compose.prod.yml ]; then
  echo "docker-compose.prod.yml not found"; exit 1
fi

if [ -z "$1" ]; then
  echo "No destination argument provided"; exit 1
fi

remote_directory='~/birding'

ssh $1 "mkdir -p $remote_directory"

scp ./docker-compose.yml $1:$remote_directory/docker-compose.yml
scp ./docker-compose.prod.yml $1:$remote_directory/docker-compose.prod.yml

rsync -rav -e ssh --exclude '*.DS_Store' --exclude '*.pyc' ./web-service $1:$remote_directory

ssh $1 "cd $remote_directory && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build birding-web-service"
