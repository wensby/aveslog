#!/bin/bash

if [ -z "$1" ]; then
  echo "No destination argument provided"; exit 1
fi

remote_directory='~/birding'

ssh $1 "mkdir -p $remote_directory && mkdir -p $remote_directory/data"

scp ./convert.py $1:$remote_directory/convert.py

ssh $1 "cd $remote_directory && python3.6 convert.py"
