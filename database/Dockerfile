FROM postgres
VOLUME /var/lib/postgresql/data
COPY index.sql /docker-entrypoint-initdb.d/
COPY schema/ /schema
