from hashlib import pbkdf2_hmac
import binascii
import os
import re
from typing import Optional, Union, Any, List, TypeVar, Type
from sqlalchemy.orm import Session
from .sqlalchemy_database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

from birding.database import Database
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


class Account(Base):
  __tablename__ = 'account'
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  email = Column(String, nullable=False)
  birder_id = Column(Integer, ForeignKey('birder.id'))
  locale_id = Column(Integer, nullable=True)

  def __eq__(self, other):
    if isinstance(other, Account):
      return (
            self.id == other.id and
            self.username == other.username and
            self.email == other.email and
            self.birder_id == other.birder_id and
            self.locale_id == other.locale_id
      )
    return False

  def __repr__(self):
    return (f"<Account(username='{self.username}', email='{self.email}', "
            f"birder_id='{self.birder_id}', locale_id='{self.locale_id}')>")


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


class HashedPassword(Base):
  __tablename__ = 'hashed_password'
  account_id = Column(Integer, ForeignKey('account.id'), primary_key=True)
  salt = Column(String, nullable=False)
  salted_hash = Column(String, nullable=False)


class TokenFactory:

  def create_token(self):
    return os.urandom(16).hex()


class AccountRepository:

  def __init__(self,
        database: Database,
        password_hasher: PasswordHasher,
        token_factory: TokenFactory,
        sqlalchemy_session: Session,
  ):
    self.database = database
    self.hasher = password_hasher
    self.token_factory = token_factory
    self.session = sqlalchemy_session

  def add(self, account: Account) -> Account:
    self.session.add(account)
    self.session.commit()
    return account

  def account_by_id(self, account_id: int) -> Optional[Account]:
    return self.session.query(Account).get(account_id)

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
    return self.session.query(Account). \
      filter(Account.username.ilike(username)).first()

  def find_account_by_email(self, email: EmailAddress) -> Optional[Account]:
    return self.session.query(Account). \
      filter(Account.email.like(email.raw)).first()

  def find_hashed_password(self, account: Account) -> Optional[HashedPassword]:
    return self.session.query(HashedPassword).filter_by(
      account_id=account.id).first()

  def set_account_birder(self, account: Account, birder: Birder) -> None:
    query = ('UPDATE account '
             'SET birder_id = %s '
             'WHERE id = %s;')
    self.database.query(query, (birder.id, account.id))

  def accounts(self) -> List[Account]:
    return self.session.query(Account).all()


class PasswordRepository:

  def __init__(self, token_factory, database, password_hasher,
        sqlalchemy_session: Session):
    self.token_factory = token_factory
    self.database = database
    self.hasher = password_hasher
    self.session = sqlalchemy_session

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

  def add(self, hashed_password: HashedPassword):
    self.session.add(hashed_password)
    self.session.commit()


class AccountFactory:

  def __init__(self,
        password_hasher: PasswordHasher,
        account_repository: AccountRepository,
        password_repository: PasswordRepository,
  ):
    self.password_hasher = password_hasher
    self.account_repository = account_repository
    self.password_repository = password_repository

  def create_account(self,
        email: EmailAddress,
        credentials: Credentials) -> Optional[Account]:
    if self.account_repository.find_account(credentials.username.raw):
      return
    account = Account(username=credentials.username.raw, email=email.raw)
    account = self.account_repository.add(account)
    salt_hashed_password = self.password_hasher.create_salt_hashed_password(
      credentials.password)
    salt = salt_hashed_password[0]
    hash = salt_hashed_password[1]
    hashed_password = HashedPassword(
      account_id=account.id, salt=salt, salted_hash=hash)
    self.password_repository.add(hashed_password)
    return account


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
