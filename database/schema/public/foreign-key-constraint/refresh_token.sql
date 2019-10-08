ALTER TABLE ONLY refresh_token
  ADD CONSTRAINT refresh_token_account_id_foreign_key
    FOREIGN KEY (account_id) REFERENCES account(id);
