CREATE TABLE password_reset_token (
  account_id INTEGER,
  token TEXT,
  PRIMARY KEY (account_id),
  CONSTRAINT password_reset_token_account_id_not_null CHECK (account_id IS NOT NULL),
  CONSTRAINT password_reset_token_token_not_null CHECK (token IS NOT NULL),
  CONSTRAINT password_reset_token_token_not_unique UNIQUE (token)
);
