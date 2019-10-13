DELETE FROM refresh_token
WHERE id = %(id)s
RETURNING id, token, account_id, expiration_date;