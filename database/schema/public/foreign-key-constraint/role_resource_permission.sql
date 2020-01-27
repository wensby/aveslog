ALTER TABLE ONLY role_resource_permission
  ADD CONSTRAINT role_resource_permission_role_id
    FOREIGN KEY (role_id) REFERENCES role(id),
  ADD CONSTRAINT role_resource_permission_resource_permission_id
    FOREIGN KEY (resource_permission_id) REFERENCES resource_permission(id);
