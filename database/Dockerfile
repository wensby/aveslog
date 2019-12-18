FROM postgres

ENV POSTGISV 2.5

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  postgresql-$PG_MAJOR-postgis-$POSTGISV \
  postgresql-$PG_MAJOR-postgis-$POSTGISV-scripts

VOLUME /var/lib/postgresql/data
COPY *.sql /docker-entrypoint-initdb.d/
COPY schema/ /schema
