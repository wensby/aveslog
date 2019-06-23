ALTER TABLE ONLY password_reset_token
  ADD CONSTRAINT password_reset_token_user_account_id_foreign_key
    FOREIGN KEY (user_account_id) REFERENCES user_account(id);
