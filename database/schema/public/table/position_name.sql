CREATE TABLE position_name (
  id SERIAL,
  position_id INTEGER,
  locale_id INTEGER,
  detail_level INTEGER,
  name TEXT,
  creation_time TIMESTAMP,
  CONSTRAINT position_name_id_primary_key PRIMARY KEY (id),
  CONSTRAINT position_name_position_id_not_null CHECK (position_id IS NOT NULL),
  CONSTRAINT position_name_locale_id_not_null CHECK (locale_id IS NOT NULL),
  CONSTRAINT position_name_name_not_null CHECK (name IS NOT NULL),
  CONSTRAINT position_name_creation_time_not_null CHECK (creation_time IS NOT NULL)
);
