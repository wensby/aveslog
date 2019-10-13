SELECT id, token, account_id, expiration_date
FROM refresh_token
WHERE id = %(id)s;