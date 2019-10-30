SELECT
  id,
  username,
  email,
  birder_id,
  locale_id
FROM
  account
WHERE
  id = %s;