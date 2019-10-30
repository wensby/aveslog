ALTER TABLE ONLY account
  ADD CONSTRAINT account_birder_id_foreign_key
    FOREIGN KEY (birder_id) REFERENCES birder(id),
  ADD CONSTRAINT account_locale_id_foreign_key
    FOREIGN KEY (locale_id) REFERENCES locale(id);
