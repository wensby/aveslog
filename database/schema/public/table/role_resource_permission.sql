CREATE TABLE role_resource_permission (
  role_id INTEGER,
  resource_permission_id INTEGER,
  CONSTRAINT role_resource_permission_primary_key PRIMARY KEY (role_id, resource_permission_id),
  CONSTRAINT role_resource_permission_role_id_not_null CHECK (role_id IS NOT NULL),
  CONSTRAINT role_resource_permission_resource_permission_id_not_null CHECK (resource_permission_id IS NOT NULL)
);
