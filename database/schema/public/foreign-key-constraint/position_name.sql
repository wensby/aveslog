ALTER TABLE ONLY position_name
  ADD CONSTRAINT position_name_position_id_foreign_key
    FOREIGN KEY (position_id) REFERENCES position(id),
  ADD CONSTRAINT position_name_locale_id_foreign_key
    FOREIGN KEY (locale_id) REFERENCES locale(id);
