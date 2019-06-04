#!/bin/bash

# Setup new backup directory
backup_dir=$(date '+%Y%m%d_%H%M%S')
mkdir $backup_dir

# Backup web service images
docker cp birding-web-service:/src/birding/static/image $backup_dir
docker exec birding-database-service \
  pg_dump -c -U postgres birding-database > $backup_dir/dump.sql
