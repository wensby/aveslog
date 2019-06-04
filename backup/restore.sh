#!/bin/bash

if [ -z "$1" ]; then
  echo "No backup directory provided"; exit 1;
fi

backup_dir=$1
docker cp $backup_dir/image/* birding-web-service:/src/birding/static/image/
cat $backup_dir/dump.sql | docker exec -i birding-database-service \
  psql -U postgres -d birding-database
