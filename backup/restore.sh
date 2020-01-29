#!/bin/bash

if [ -z "$1" ]; then
  echo "No backup directory provided"; exit 1;
fi

backup_dir=$1
docker cp $backup_dir/backup.dump database-service:/backup.dump
docker exec -i database-service \
  pg_restore -U postgres -d birding-database \
  -v --clean --if-exists \
  /backup.dump
