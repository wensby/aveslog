DELETE FROM refresh_token
WHERE account_id = %(account_id)s
RETURNING id, token, account_id, expiration_date;