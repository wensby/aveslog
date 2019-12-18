ALTER TABLE ONLY sighting
  ADD CONSTRAINT sighting_birder_id_foreign_key
    FOREIGN KEY (birder_id) REFERENCES birder(id),
  ADD CONSTRAINT sighting_bird_id_foreign_key
    FOREIGN KEY (bird_id) REFERENCES bird(id),
  ADD CONSTRAINT sighting_position_id_foreign_key
    FOREIGN KEY (position_id) REFERENCES position(id);
