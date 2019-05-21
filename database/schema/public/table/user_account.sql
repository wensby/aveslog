CREATE TABLE user_account (
  id SERIAL,
  username TEXT,
  email TEXT,
  person_id INTEGER,
  locale_id INTEGER,
  CONSTRAINT user_account_id_primary_key PRIMARY KEY (id),
  CONSTRAINT user_account_username_not_null CHECK (username IS NOT NULL),
  CONSTRAINT user_account_email_not_null CHECK (email IS NOT NULL),
  FOREIGN KEY (person_id) REFERENCES person (id)
);
