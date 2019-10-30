CREATE TABLE sighting (
  id SERIAL,
  birder_id INTEGER,
  bird_id INTEGER,
  sighting_date DATE,
  sighting_time TIME WITHOUT TIME ZONE,
  CONSTRAINT sighting_id_primary_key PRIMARY KEY (id),
  CONSTRAINT sighting_date_not_null CHECK (sighting_date IS NOT NULL)
);
