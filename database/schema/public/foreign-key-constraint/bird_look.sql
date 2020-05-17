ALTER TABLE ONLY bird_look
  ADD CONSTRAINT bird_look_bird_id_foreign_key
    FOREIGN KEY (bird_id) REFERENCES bird(id);
