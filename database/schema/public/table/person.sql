CREATE TABLE person (
  id serial,
  name text,
  CONSTRAINT person_id_primary_key PRIMARY KEY (id),
  CONSTRAINT person_name_not_null CHECK(name IS NOT NULL)
);
