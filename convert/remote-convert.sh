#!/bin/bash

if [ -z "$1" ]; then
  echo "No destination argument provided"; exit 1;
fi

remote_host=$1
remote_directory='~/birding'

# Copy over required directories to build and start the application
rsync -rav -e ssh --exclude-from ./convert/rsync-exclude-list.txt \
  ./convert $remote_host:$remote_directory

# Change to correct directory and run deploy production script on remote
ssh $remote_host "cd $remote_directory && ./convert/convert.sh"
