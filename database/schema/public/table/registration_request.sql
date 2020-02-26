CREATE TABLE registration_request (
  id SERIAL,
  email TEXT,
  token TEXT,
  CONSTRAINT registration_request_id_primary_key PRIMARY KEY (id),
  CONSTRAINT registration_request_email_not_null CHECK (email IS NOT NULL),
  CONSTRAINT registration_request_email_unique UNIQUE (email),
  CONSTRAINT registration_request_token_not_null CHECK (token IS NOT NULL),
  CONSTRAINT registration_request_token_unique UNIQUE (token)
);
