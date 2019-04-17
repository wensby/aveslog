CREATE TABLE sighting (
  id SERIAL,
  person_id INTEGER,
  bird_id INTEGER,
  CONSTRAINT sighting_id_primary_key PRIMARY KEY (id),
  FOREIGN KEY (person_id) REFERENCES person (id),
  FOREIGN KEY (bird_id) REFERENCES bird (id)
);
