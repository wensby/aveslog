ALTER TABLE ONLY birder_connection
  ADD CONSTRAINT birder_connection_birder_id_foreign_key
    FOREIGN KEY (birder_id) REFERENCES birder(id),
  ADD CONSTRAINT birder_connection_connection_birder_id_foreign_key
    FOREIGN KEY (connection_birder_id) REFERENCES birder(id);
