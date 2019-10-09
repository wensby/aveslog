UPDATE refresh_token
SET
  token = %(token)s,
  account_id = %(account_id)s,
  expiration_date = %(expiration_date)s
WHERE id = %(id)s
RETURNING id, token, account_id, expiration_date;