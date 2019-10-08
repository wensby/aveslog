SELECT
  id,
  username,
  email,
  person_id,
  locale_id
FROM
  account
WHERE
  id = %s;