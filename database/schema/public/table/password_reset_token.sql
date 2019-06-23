CREATE TABLE password_reset_token (
  user_account_id INTEGER,
  token TEXT,
  CONSTRAINT password_reset_token_user_account_id_not_null CHECK (user_account_id IS NOT NULL),
  CONSTRAINT password_reset_token_token_not_null CHECK (token IS NOT NULL),
  CONSTRAINT password_reset_token_token_not_unique UNIQUE (token),
  PRIMARY KEY (user_account_id)
);
