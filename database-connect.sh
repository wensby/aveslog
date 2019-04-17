#!/bin/sh

docker exec --tty --interactive birding-database-service \
  psql -h localhost -U postgres -d birding-database
