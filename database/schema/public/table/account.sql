CREATE TABLE account (
  id SERIAL,
  username TEXT,
  email TEXT,
  birder_id INTEGER,
  locale_id INTEGER,
  creation_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT account_id_primary_key PRIMARY KEY (id),
  CONSTRAINT account_username_not_null CHECK (username IS NOT NULL),
  CONSTRAINT account_email_not_null CHECK (email IS NOT NULL),
  CONSTRAINT account_email_unique UNIQUE (email),
  CONSTRAINT account_creation_datetime_not_null CHECK (creation_datetime IS NOT NULL)
);
