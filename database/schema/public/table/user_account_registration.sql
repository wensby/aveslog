CREATE TABLE user_account_registration (
  id SERIAL,
  email TEXT,
  token TEXT,
  CONSTRAINT user_account_registration_id_primary_key PRIMARY KEY (id),
  CONSTRAINT user_account_registration_email_not_null CHECK (email IS NOT NULL),
  CONSTRAINT user_account_registration_email_unique UNIQUE (email),
  CONSTRAINT user_account_registration_token_not_null CHECK (token IS NOT NULL),
  CONSTRAINT user_account_registration_token_unique UNIQUE (token)
);
