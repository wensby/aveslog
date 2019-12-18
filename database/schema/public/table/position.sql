CREATE TABLE position (
  id SERIAL,
  point GEOGRAPHY(POINT),
  CONSTRAINT position_id_primary_key PRIMARY KEY (id),
  CONSTRAINT position_point_not_null CHECK (point IS NOT NULL)
);
