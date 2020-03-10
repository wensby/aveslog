CREATE TABLE birder_connection (
  birder_id INTEGER,
  connection_birder_id INTEGER,
  CONSTRAINT birder_connection_primary_key PRIMARY KEY (birder_id, connection_birder_id),
  CONSTRAINT birder_connection_birder_id_not_null CHECK (birder_id IS NOT NULL),
  CONSTRAINT birder_connection_connection_birder_id_not_null CHECK (connection_birder_id IS NOT NULL)
);
