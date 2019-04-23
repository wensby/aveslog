CREATE TABLE hashed_password (
  user_account_id INTEGER,
  salt TEXT,
  salted_hash TEXT,
  CONSTRAINT user_account_id_not_null CHECK (user_account_id IS NOT NULL),
  FOREIGN KEY (user_account_id) REFERENCES user_account (id),
  CONSTRAINT salt_not_null CHECK (salt IS NOT NULL),
  CONSTRAINT salted_hash_not_null CHECK (salted_hash IS NOT NULL)
);
