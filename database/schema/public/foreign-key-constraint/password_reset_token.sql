ALTER TABLE ONLY password_reset_token
  ADD CONSTRAINT password_reset_token_account_id_foreign_key
    FOREIGN KEY (account_id) REFERENCES account(id);
