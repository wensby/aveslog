#!/bin/sh

docker exec --tty --interactive database-service \
  psql -h localhost -U postgres -d birding-database
