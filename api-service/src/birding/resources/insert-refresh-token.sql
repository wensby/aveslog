INSERT INTO refresh_token (token, account_id, expiration_date)
VALUES (%(token)s, %(account_id)s, %(expiration_date)s)
RETURNING id, token, account_id, expiration_date;