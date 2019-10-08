ALTER TABLE ONLY account
  ADD CONSTRAINT account_person_id_foreign_key
    FOREIGN KEY (person_id) REFERENCES person(id),
  ADD CONSTRAINT account_locale_id_foreign_key
    FOREIGN KEY (locale_id) REFERENCES locale(id);
