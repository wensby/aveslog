from hashlib import pbkdf2_hmac
import binascii
import os
import re
from typing import Optional, Union, Any, List, TypeVar, Type

from birding.database import Database
from .database import read_script_file
from birding.mail import EmailAddress
from birding.birder import Birder


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

  def __init__(self, account_id, username, email, birder_id, locale_id):
    self.id = account_id
    self.username = username
    self.email = email
    self.birder_id = birder_id
    self.locale_id = locale_id

  def __eq__(self, other):
    if isinstance(other, Account):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self):
    return (f'Account({self.id}, {self.username}, {self.email}, '
            f'{self.birder_id}, {self.locale_id})')


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
        'SELECT 1 FROM account WHERE username LIKE %s;',
        (credentials.username.raw,))
      if len(result.rows) > 0:
        return
      result = transaction.execute(
        ('INSERT INTO account (username, email) '
         'VALUES (%s, %s) '
         'RETURNING id, username, email, birder_id, locale_id;'),
        (credentials.username.raw, email.raw))
      account = next(map(Account.fromrow, result.rows), None)
      if not account:
        return
      salt_hashed_password = self.hasher.create_salt_hashed_password(
        credentials.password)
      salt = salt_hashed_password[0]
      hash = salt_hashed_password[1]
      transaction.execute(
        'INSERT INTO hashed_password (account_id, salt, salted_hash) '
        'VALUES (%s, %s, %s);', (account.id, salt, hash))
      return account


AccountRegistrationType = TypeVar(
  'AccountRegistrationType', bound='AccountRegistration')


class AccountRegistration:

  def __init__(self, account_registration_id: int, email: str, token: str):
    self.id = account_registration_id
    self.email = email
    self.token = token

  @classmethod
  def fromrow(cls: Type[AccountRegistrationType],
        row: list) -> AccountRegistrationType:
    return cls(row[0], row[1], row[2])


class HashedPassword:

  def __init__(self, account_id, salt, salted_hash):
    self.account_id = account_id
    self.salt = salt
    self.salted_hash = salted_hash

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2])


class TokenFactory:

  def create_token(self):
    return os.urandom(16).hex()


class AccountRepository:

  def __init__(self,
        database: Database,
        password_hasher: PasswordHasher,
        token_factory: TokenFactory):
    self.database = database
    self.hasher = password_hasher
    self.token_factory = token_factory

  def account_by_id(self, account_id: int) -> Optional[Account]:
    with self.database.transaction() as transaction:
      query = read_script_file('select-account-by-id.sql')
      result = transaction.execute(query, (account_id,), Account.fromrow)
      if not result.rows:
        return None
      return result.rows[0]

  def remove_account_registration_by_id(self, account_id: int) -> None:
    query = ('DELETE FROM account_registration '
             'WHERE id = %s;')
    self.database.query(query, (account_id,))

  def create_account_registration(self,
        email: EmailAddress) -> Optional[AccountRegistration]:
    token = self.token_factory.create_token()
    query = (
      'INSERT INTO account_registration (email, token) '
      'VALUES (%s, %s) '
      'ON CONFLICT (email) DO UPDATE SET token = EXCLUDED.token '
      'RETURNING id, email, token;')
    result = self.database.query(query, (email.raw, token))
    return next(map(AccountRegistration.fromrow, result.rows), None)

  def find_account_registration(self,
        email: EmailAddress,
        token: str) -> Optional[AccountRegistration]:
    query = ('SELECT id, email, token '
             'FROM account_registration '
             'WHERE email LIKE %s AND token LIKE %s;')
    result = self.database.query(query, (email.raw, token))
    return next(map(AccountRegistration.fromrow, result.rows), None)

  def find_account_registration_by_token(self,
        token: str) -> Optional[AccountRegistration]:
    query = ('SELECT id, email, token '
             'FROM account_registration '
             'WHERE token LIKE %s;')
    result = self.database.query(query, (token,))
    return next(map(AccountRegistration.fromrow, result.rows), None)

  def find_account(self,
        username: Union[Username, str]) -> Optional[Account]:
    if isinstance(username, Username):
      username = username.raw
    query = ('SELECT id, username, email, birder_id, locale_id '
             'FROM account '
             'WHERE username ILIKE %s;')
    result = self.database.query(query, (username,))
    return next(map(Account.fromrow, result.rows), None)

  def find_account_by_email(self, email: EmailAddress) -> Optional[Account]:
    query = ('SELECT id, username, email, birder_id, locale_id '
             'FROM account '
             'WHERE email LIKE %s;')
    result = self.database.query(query, (email.raw,))
    return next(map(Account.fromrow, result.rows), None)

  def find_hashed_password(self, account: Account) -> Optional[HashedPassword]:
    query = ('SELECT account_id, salt, salted_hash '
             'FROM hashed_password '
             'WHERE account_id = %s;')
    result = self.database.query(query, (account.id,))
    return next(map(HashedPassword.fromrow, result.rows), None)

  def set_account_birder(self, account: Account, birder: Birder) -> None:
    query = ('UPDATE account '
             'SET birder_id = %s '
             'WHERE id = %s;')
    self.database.query(query, (birder.id, account.id))

  def accounts(self) -> List[Account]:
    with self.database.transaction() as transaction:
      query = read_script_file('select-accounts.sql')
      return transaction.execute(query, mapper=Account.fromrow).rows


class PasswordRepository:

  def __init__(self, token_factory, database, password_hasher):
    self.token_factory = token_factory
    self.database = database
    self.hasher = password_hasher

  def create_password_reset_token(self, account):
    token = self.token_factory.create_token()
    query = (
      'INSERT INTO password_reset_token (account_id, token) '
      'VALUES (%s, %s) '
      'ON CONFLICT (account_id) '
      'DO UPDATE SET token = excluded.token;')
    result = self.database.query(query, (account.id, token))
    if 'INSERT' in result.status:
      return self.find_password_reset_token(account)

  def find_password_reset_token(self, account):
    query = (
      'SELECT account_id, token '
      'FROM password_reset_token '
      'WHERE account_id = %s;')
    result = self.database.query(query, (account.id,))
    return next(map(PasswordResetToken.fromrow, result.rows), None)

  def find_password_reset_account_id(self, token):
    query = (
      'SELECT account_id '
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
             'WHERE account_id = %s;')
    self.database.query(query, (salt, hash, account_id))

  def remove_password_reset_token(self, token):
    query = (
      'DELETE FROM password_reset_token '
      'WHERE token LIKE %s;')
    self.database.query(query, (token,))


class PasswordResetToken:

  def __init__(self, account_id, token):
    self.account_id = account_id
    self.token = token

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1])

  def __repr__(self):
    return f'{self.__class__.__name__}({self.account_id}, {self.token})'

  def __eq__(self, other):
    if isinstance(other, PasswordResetToken):
      return self.__dict__ == other.__dict__
    return False
