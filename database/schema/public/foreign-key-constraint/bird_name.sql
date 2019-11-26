ALTER TABLE ONLY bird_name
  ADD CONSTRAINT bird_name_bird_id_foreign_key
    FOREIGN KEY (bird_id) REFERENCES bird(id),
  ADD CONSTRAINT bird_name_locale_id_foreign_key
    FOREIGN KEY (locale_id) REFERENCES locale(id);
