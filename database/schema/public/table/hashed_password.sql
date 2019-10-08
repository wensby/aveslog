CREATE TABLE hashed_password (
  account_id INTEGER,
  salt TEXT,
  salted_hash TEXT,
  CONSTRAINT account_id_not_null CHECK (account_id IS NOT NULL),
  CONSTRAINT salt_not_null CHECK (salt IS NOT NULL),
  CONSTRAINT salted_hash_not_null CHECK (salted_hash IS NOT NULL)
);
