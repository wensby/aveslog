CREATE TABLE bird_common_name (
  id SERIAL,
  bird_id INTEGER,
  locale_id INTEGER,
  name TEXT,
  CONSTRAINT bird_common_name_id_primary_key PRIMARY KEY (id),
  CONSTRAINT bird_common_name_bird_id_not_null CHECK (bird_id IS NOT NULL),
  CONSTRAINT bird_common_name_locale_id_not_null CHECK (locale_id IS NOT NULL),
  CONSTRAINT bird_common_name_name_not_null CHECK (name IS NOT NULL),
  CONSTRAINT bird_common_name_name_not_empty CHECK (name <> '')
);
