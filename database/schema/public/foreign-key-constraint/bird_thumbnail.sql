ALTER TABLE ONLY bird_thumbnail
  ADD CONSTRAINT bird_thumbnail_bird_id_foreign_key
    FOREIGN KEY (bird_id) REFERENCES bird(id),
  ADD CONSTRAINT bird_thumbnail_picture_id_foreign_key
    FOREIGN KEY (picture_id) REFERENCES picture(id);
