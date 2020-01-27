ALTER TABLE ONLY account_role
  ADD CONSTRAINT account_role_account_id_foreign_key
    FOREIGN KEY (account_id) REFERENCES account(id),
  ADD CONSTRAINT account_role_role_id_foreign_key
    FOREIGN KEY (role_id) REFERENCES role(id);
