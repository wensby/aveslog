#!/bin/bash

if [ -z "$1" ]; then
  echo "No destination argument provided"; exit 1;
fi

remote_host=$1
remote_directory='~/birding'
ssh $remote_host "mkdir -p $remote_directory"

# Copy over required directories to build and start the application
rsync -rav -e ssh --exclude-from ./deploy/rsync-exclude-list.txt \
  ./docker-compose.yml ./docker-compose.prod.yml \
  $remote_host:$remote_directory

rsync -rav -e ssh --delete --exclude-from ./deploy/rsync-exclude-list.txt \
  ./deploy ./web-service ./database ./backup \
  $remote_host:$remote_directory

# Change to correct directory and run deploy production script on remote
ssh $remote_host "cd $remote_directory && ./deploy/production-startup.sh"
