ALTER TABLE ONLY user_account
ADD CONSTRAINT user_account_locale_id_foreign_key
FOREIGN KEY (locale_id) REFERENCES locale(id);
