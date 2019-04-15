#!/bin/bash

python3.6 convert/convert_bird_data.py
docker cp convert/insert-bird.sql \
  birding-database-service:/convert/insert-bird.sql
docker exec -u postgres birding-database-service \
  psql "birding-database" postgres \
  -f convert/insert-bird.sql
