CREATE TABLE locale (
  id SERIAL,
  code TEXT,
  CONSTRAINT locale_id_primary_key PRIMARY KEY (id),
  CONSTRAINT locale_code_not_null CHECK (code IS NOT NULL),
  CONSTRAINT locale_code_unique UNIQUE (code)
);
