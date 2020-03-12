CREATE TABLE birder_connection (
  id SERIAL,
  primary_birder_id INTEGER,
  secondary_birder_id INTEGER,
  modification_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT birder_connection_id_primary_key
    PRIMARY KEY (id),
  CONSTRAINT birder_connection_primary_birder_id_not_null
    CHECK (primary_birder_id IS NOT NULL),
  CONSTRAINT birder_connection_secondary_birder_id_not_null
    CHECK (secondary_birder_id IS NOT NULL),
  CONSTRAINT birder_connection_birder_ids_unique
    UNIQUE (primary_birder_id, secondary_birder_id),
  CONSTRAINT birder_connection_modification_datetime_not_null
    CHECK (modification_datetime IS NOT NULL)
);
