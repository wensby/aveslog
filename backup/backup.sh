#!/bin/bash

# Setup new backup directory
backup_dir=$(date '+%Y%m%d_%H%M%S')
mkdir $backup_dir

# Backup web service images
docker exec database-service \
  pg_dump -Fc -U postgres birding-database > $backup_dir/backup.dump
