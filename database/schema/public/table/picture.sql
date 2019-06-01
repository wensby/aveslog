CREATE TABLE picture (
  id SERIAL,
  filepath TEXT,
  credit TEXT,
  CONSTRAINT picture_id_primary_key PRIMARY KEY (id),
  CONSTRAINT picture_filepath_not_null CHECK(filepath IS NOT NULL)
);
