FROM postgres

ENV POSTGRES_DB=birding-database
ENV POSTGRES_PASSWORD=docker

VOLUME /var/lib/postgresql/data

COPY index.sql /docker-entrypoint-initdb.d/

COPY schema/ /schema
