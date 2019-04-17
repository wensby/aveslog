#!/bin/bash

python3.6 convert/convert_person_data.py
python3.6 convert/convert_sighting_data.py

docker cp convert/insert-person.sql \
  birding-database-service:/convert/insert-person.sql
docker cp convert/insert-sighting.sql \
  birding-database-service:/convert/insert-sighting.sql

docker exec -u postgres birding-database-service \
  psql "birding-database" postgres \
  -f /schema/public/table/person.sql
docker exec -u postgres birding-database-service \
  psql "birding-database" postgres \
  -f /schema/public/table/sighting.sql
docker exec -u postgres birding-database-service \
  psql "birding-database" postgres \
  -f convert/insert-person.sql
docker exec -u postgres birding-database-service \
  psql "birding-database" postgres \
  -f convert/insert-sighting.sql

rm -rf data/*
rmdir data
