#!/bin/bash

# --- Parse options --- #

POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -s|--service)
      SERVICE="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      POSITIONAL+=("$1")
      shift # past argument
      ;;
  esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if ! [ -z "$SERVICE" ]; then
  echo "SERVICE = $SERVICE"
fi

if [ -z "$1" ]; then
  echo "No destination argument provided"; exit 1;
fi

remote_host=$1
remote_directory='~/birding'
ssh $remote_host "mkdir -p $remote_directory"

# Copy over required directories to build and start the application
rsync -rav -e ssh --exclude-from ./remote/rsync-exclude-list.txt \
  ./.env ./docker-compose.yml ./docker-compose.prod.yml \
  $remote_host:$remote_directory

rsync -rav -e ssh --delete --exclude-from ./remote/rsync-exclude-list.txt \
  ./remote ./api-service ./database ./backup ./frontend-service \
  $remote_host:$remote_directory

# Change to correct directory and run deploy production script on remote
ssh $remote_host "cd $remote_directory && ./remote/production-startup.sh $SERVICE"
