CREATE TABLE account_registration (
  id SERIAL,
  email TEXT,
  token TEXT,
  CONSTRAINT account_registration_id_primary_key PRIMARY KEY (id),
  CONSTRAINT account_registration_email_not_null CHECK (email IS NOT NULL),
  CONSTRAINT account_registration_email_unique UNIQUE (email),
  CONSTRAINT account_registration_token_not_null CHECK (token IS NOT NULL),
  CONSTRAINT account_registration_token_unique UNIQUE (token)
);
