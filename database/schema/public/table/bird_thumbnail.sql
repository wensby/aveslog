CREATE TABLE bird_thumbnail (
  bird_id INTEGER,
  picture_id INTEGER,
  CONSTRAINT bird_thumbnail_bird_id_not_null CHECK (bird_id IS NOT NULL),
  CONSTRAINT bird_thumbnail_picture_id_not_null CHECK (picture_id IS NOT NULL),
  PRIMARY KEY (bird_id)
);
