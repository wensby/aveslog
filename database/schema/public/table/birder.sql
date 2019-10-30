CREATE TABLE birder (
  id serial,
  name text,
  CONSTRAINT birder_id_primary_key PRIMARY KEY (id),
  CONSTRAINT birder_name_not_null CHECK(name IS NOT NULL)
);
