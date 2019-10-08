CREATE TABLE account (
  id SERIAL,
  username TEXT,
  email TEXT,
  person_id INTEGER,
  locale_id INTEGER,
  CONSTRAINT account_id_primary_key PRIMARY KEY (id),
  CONSTRAINT account_username_not_null CHECK (username IS NOT NULL),
  CONSTRAINT account_email_not_null CHECK (email IS NOT NULL),
  CONSTRAINT account_email_unique UNIQUE (email)
);
