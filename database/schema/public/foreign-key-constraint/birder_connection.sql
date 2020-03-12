ALTER TABLE ONLY birder_connection
  ADD CONSTRAINT birder_connection_primary_birder_id_foreign_key
    FOREIGN KEY (primary_birder_id) REFERENCES birder(id),
  ADD CONSTRAINT birder_connection_secondary_birder_id_foreign_key
    FOREIGN KEY (secondary_birder_id) REFERENCES birder(id);
