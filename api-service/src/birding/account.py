from hashlib import pbkdf2_hmac
import binascii
import os
import re
from typing import Optional, Union, Any

from birding.database import Database
from birding.mail import EmailAddress


class Username:
  regex = re.compile('^[A-Za-z0-9_.-]{5,32}$')

  @classmethod
  def is_valid(cls, raw_username):
    return cls.regex.match(raw_username)

  def __init__(self, raw_username):
    if not self.is_valid(raw_username):
      raise Exception(f'Username format invalid: {raw_username}')
    self.raw = raw_username

  def __eq__(self, other):
    if isinstance(other, Username):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self.raw})'


class Password:
  regex = re.compile('^.{8,128}$')

  @classmethod
  def is_valid(cls, raw_password):
    return cls.regex.match(raw_password)

  def __init__(self, raw_password):
    if not self.is_valid(raw_password):
      raise Exception(f'Password format invalid: {raw_password}')
    self.raw = raw_password

  def __eq__(self, other):
    if isinstance(other, Password):
      return self.__dict__ == other.__dict__
    return False


class Credentials:

  def __init__(self, username: Username, password: Password) -> None:
    self.username: Username = username
    self.password: Password = password

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, Credentials):
      return self.__dict__ == other.__dict__
    return False


class Account:

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2], row[3], row[4])

  def __init__(self, account_id, username, email, person_id, locale_id):
    self.id = account_id
    self.username = username
    self.email = email
    self.person_id = person_id
    self.locale_id = locale_id

  def __eq__(self, other):
    if isinstance(other, Account):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self):
    return (f'Account({self.id}, {self.username}, {self.email}, '
            f'{self.person_id}, {self.locale_id})')


class PasswordHasher:

  def __init__(self, salt_factory):
    self.salt_factory = salt_factory

  def create_salt_hashed_password(self, password):
    salt = self.salt_factory.create_salt()
    hash = self.hash_password(password, salt)
    return (salt, hash)

  def hash_password(self, password: Union[Password, str], salt: str) -> str:
    if isinstance(password, Password):
      password = password.raw
    encoded_password = password.encode()
    encoded_salt = salt.encode()
    binary_hash = pbkdf2_hmac('sha256', encoded_password, encoded_salt, 100000)
    return binascii.hexlify(binary_hash).decode()


class AccountFactory:

  def __init__(self, database: Database, hasher: PasswordHasher) -> None:
    self.database: Database = database
    self.hasher: PasswordHasher = hasher

  def create_account(self,
        email: EmailAddress,
        credentials: Credentials) -> Optional[Account]:
    with self.database.transaction() as transaction:
      result = transaction.execute(
        'SELECT 1 FROM user_account WHERE username LIKE %s;',
        (credentials.username.raw,))
      if len(result.rows) > 0:
        return
      result = transaction.execute(
        ('INSERT INTO user_account (username, email) '
         'VALUES (%s, %s) '
         'RETURNING id, username, email, person_id, locale_id;'),
        (credentials.username.raw, email.raw))
      account = next(map(Account.fromrow, result.rows), None)
      if not account:
        return
      salt_hashed_password = self.hasher.create_salt_hashed_password(
        credentials.password)
      salt = salt_hashed_password[0]
      hash = salt_hashed_password[1]
      transaction.execute(
        'INSERT INTO hashed_password (user_account_id, salt, salted_hash) '
        'VALUES (%s, %s, %s);', (account.id, salt, hash))
      return account


class AccountRegistration:

  def __init__(self, id, email, token):
    self.id = id
    self.email = email
    self.token = token

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2])


class HashedPassword:

  def __init__(self, user_account_id, salt, salted_hash):
    self.user_account_id = user_account_id
    self.salt = salt
    self.salted_hash = salted_hash

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2])


class AccountRepository:

  def __init__(self, database: Database, password_hasher, token_factory):
    self.database = database
    self.hasher = password_hasher
    self.token_factory = token_factory

  def find_account_by_id(self, id) -> Account:
    with self.database.transaction() as transaction:
      query = ('SELECT id, username, email, person_id, locale_id '
               'FROM user_account '
               'WHERE id = %s;')
      result = transaction.execute(query, (id,), Account.fromrow)
      return next(iter(result.rows), None)

  def remove_account_registration_by_id(self, id):
    query = ('DELETE FROM user_account_registration '
             'WHERE id = %s;')
    self.database.query(query, (id,))

  def create_account_registration(self, email):
    token = self.token_factory.create_token()
    query = (
      'INSERT INTO user_account_registration (email, token) '
      'VALUES (%s, %s) '
      'ON CONFLICT (email) DO UPDATE SET token = EXCLUDED.token '
      'RETURNING id, email, token;')
    result = self.database.query(query, (email.raw, token))
    return next(map(AccountRegistration.fromrow, result.rows), None)

  def find_account_registration(self, email, token):
    query = ('SELECT id, email, token '
             'FROM user_account_registration '
             'WHERE email LIKE %s AND token LIKE %s;')
    result = self.database.query(query, (email.raw, token))
    return next(map(AccountRegistration.fromrow, result.rows), None)

  def find_account_registration_by_token(
        self, token: str) -> Optional[AccountRegistration]:
    query = ('SELECT id, email, token '
             'FROM user_account_registration '
             'WHERE token LIKE %s;')
    result = self.database.query(query, (token,))
    return next(map(AccountRegistration.fromrow, result.rows), None)

  def find_user_account(self,
        username: Union[Username, str]) -> Optional[Account]:
    if isinstance(username, Username):
      username = username.raw
    query = ('SELECT id, username, email, person_id, locale_id '
             'FROM user_account '
             'WHERE username ILIKE %s;')
    result = self.database.query(query, (username,))
    return next(map(Account.fromrow, result.rows), None)

  def find_account_by_email(self, email):
    query = ('SELECT id, username, email, person_id, locale_id '
             'FROM user_account '
             'WHERE email LIKE %s;')
    result = self.database.query(query, (email.raw,))
    return next(map(Account.fromrow, result.rows), None)

  def find_hashed_password(self, user_account):
    query = ('SELECT user_account_id, salt, salted_hash '
             'FROM hashed_password '
             'WHERE user_account_id = %s;')
    result = self.database.query(query, (user_account.id,))
    return next(map(HashedPassword.fromrow, result.rows), None)

  def set_user_account_person(self, account, person):
    query = ('UPDATE user_account '
             'SET person_id = %s '
             'WHERE id = %s;')
    self.database.query(query, (person.id, account.id))

  def accounts(self):
    with self.database.transaction() as transaction:
      result = transaction.execute(
        'SELECT * FROM user_account;', mapper=Account.fromrow)
      return result.rows


class PasswordRepository:

  def __init__(self, token_factory, database, password_hasher):
    self.token_factory = token_factory
    self.database = database
    self.hasher = password_hasher

  def create_password_reset_token(self, account):
    token = self.token_factory.create_token()
    query = (
      'INSERT INTO password_reset_token (user_account_id, token) '
      'VALUES (%s, %s) '
      'ON CONFLICT (user_account_id) '
      'DO UPDATE SET token = excluded.token;')
    result = self.database.query(query, (account.id, token))
    if 'INSERT' in result.status:
      return self.find_password_reset_token(account)

  def find_password_reset_token(self, account):
    query = (
      'SELECT user_account_id, token '
      'FROM password_reset_token '
      'WHERE user_account_id = %s;')
    result = self.database.query(query, (account.id,))
    return next(map(PasswordResetToken.fromrow, result.rows), None)

  def find_password_reset_account_id(self, token):
    query = (
      'SELECT user_account_id '
      'FROM password_reset_token '
      'WHERE token LIKE %s;')
    result = self.database.query(query, (token,))
    return next(map(lambda row: row[0], result.rows), None)

  def update_password(self, account_id, password):
    salt_hashed_password = self.hasher.create_salt_hashed_password(password)
    salt = salt_hashed_password[0]
    hash = salt_hashed_password[1]
    query = ('UPDATE hashed_password '
             'SET salt = %s, salted_hash = %s '
             'WHERE user_account_id = %s;')
    self.database.query(query, (salt, hash, account_id))

  def remove_password_reset_token(self, token):
    query = (
      'DELETE FROM password_reset_token '
      'WHERE token LIKE %s;')
    self.database.query(query, (token,))


class PasswordResetToken:

  def __init__(self, user_account_id, token):
    self.user_account_id = user_account_id
    self.token = token

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1])

  def __repr__(self):
    return f'{self.__class__.__name__}({self.user_account_id}, {self.token})'

  def __eq__(self, other):
    if isinstance(other, PasswordResetToken):
      return self.__dict__ == other.__dict__
    return False


class TokenFactory:

  def create_token(self):
    return os.urandom(16).hex()
