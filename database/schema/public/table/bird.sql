CREATE TABLE bird (
  id SERIAL,
  binomial_name text,
  CONSTRAINT bird_id_primary_key PRIMARY KEY (id),
  CONSTRAINT bird_binomial_name_not_null CHECK(binomial_name IS NOT NULL)
);
