CREATE TABLE resource_permission (
  id SERIAL,
  name TEXT,
  resource_regex TEXT,
  method TEXT,
  CONSTRAINT resource_permission_id_primary_key PRIMARY KEY (id),
  CONSTRAINT resource_permission_resource_regex_not_null CHECK (resource_regex IS NOT NULL),
  CONSTRAINT resource_permission_method_not_null CHECK (method IS NOT NULL)
);
