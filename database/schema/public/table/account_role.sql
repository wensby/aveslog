CREATE TABLE account_role (
  account_id INTEGER,
  role_id INTEGER,
  CONSTRAINT account_role_primary_key PRIMARY KEY (account_id, role_id),
  CONSTRAINT account_role_account_id_not_null CHECK (account_id IS NOT NULL),
  CONSTRAINT account_role_role_id_not_null CHECK (role_id IS NOT NULL)
);
