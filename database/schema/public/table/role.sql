CREATE TABLE role (
  id SERIAL,
  name TEXT,
  CONSTRAINT role_id_primary_key PRIMARY KEY (id),
  CONSTRAINT role_name_not_null CHECK(name IS NOT NULL),
  CONSTRAINT role_name_unique UNIQUE (name)
);
