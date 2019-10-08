CREATE TABLE refresh_token (
  id SERIAL,
  token TEXT,
  account_id INTEGER,
  expiration_date TIMESTAMP WITHOUT TIME ZONE,
  CONSTRAINT refresh_token_id_primary_key PRIMARY KEY (id),
  CONSTRAINT refresh_token_token_not_null CHECK (token IS NOT NULL),
  CONSTRAINT refresh_token_token_unique UNIQUE (token),
  CONSTRAINT refresh_token_expiration_date_not_null CHECK (expiration_date IS NOT NULL)
);
