ALTER TABLE ONLY sighting
  ADD CONSTRAINT sighting_person_id_foreign_key
    FOREIGN KEY (person_id) REFERENCES person(id),
  ADD CONSTRAINT sighting_bird_id_foreign_key
    FOREIGN KEY (bird_id) REFERENCES bird(id);
