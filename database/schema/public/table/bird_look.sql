CREATE TABLE bird_look (
  id SERIAL,
  bird_id INTEGER,
  label TEXT,
  description TEXT,
  CONSTRAINT bird_look_id_primary_key PRIMARY KEY (id),
  CONSTRAINT bird_look_bird_id_not_null CHECK (bird_id IS NOT NULL)
);
