CREATE TABLE bird (
  id SERIAL,
  name text,
  CONSTRAINT bird_id_primary_key PRIMARY KEY (id),
  CONSTRAINT bird_name_not_null CHECK(name IS NOT NULL)
);
