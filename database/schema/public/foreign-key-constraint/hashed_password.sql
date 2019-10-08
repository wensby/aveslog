ALTER TABLE ONLY hashed_password
  ADD CONSTRAINT hashed_password_account_id_foreign_key
    FOREIGN KEY (account_id) REFERENCES account(id);
