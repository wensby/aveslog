from hashlib import pbkdf2_hmac
import binascii
import os
import re
from typing import Optional, Union, Any, List, TypeVar
from sqlalchemy.orm import Session
from aveslog.v0.models import Birder, Account, AccountRegistration, \
  HashedPassword, PasswordResetToken

from aveslog.v0.mail import EmailAddress


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


class TokenFactory:

  def create_token(self):
    return os.urandom(16).hex()


class AccountRepository:

  def __init__(self,
        password_hasher: PasswordHasher,
        sqlalchemy_session: Session,
  ):
    self.hasher = password_hasher
    self.session = sqlalchemy_session

  def add(self, account: Account) -> Account:
    self.session.add(account)
    self.session.commit()
    return account

  def account_by_id(self, account_id: int) -> Optional[Account]:
    return self.session.query(Account).get(account_id)

  def remove_account_registration_by_id(self, account_id: int) -> None:
    account_registration = self.session.query(AccountRegistration). \
      filter_by(id=account_id).first()
    self.session.delete(account_registration)
    self.session.commit()

  def add_account_registration(self,
        account_registration: AccountRegistration,
  ) -> Optional[AccountRegistration]:
    self.session.add(account_registration)
    self.session.commit()
    return account_registration

  def find_account_registration(self,
        email: EmailAddress,
        token: str,
  ) -> Optional[AccountRegistration]:
    return self.session.query(AccountRegistration). \
      filter(AccountRegistration.email.like(email.raw)). \
      filter(AccountRegistration.token.like(token)).first()

  def find_account_registration_by_token(self,
        token: str,
  ) -> Optional[AccountRegistration]:
    return self.session.query(AccountRegistration). \
      filter(AccountRegistration.token.like(token)).first()

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
    account = self.session.query(Account).filter_by(id=account.id).first()
    account.birder_id = birder.id
    self.session.commit()

  def accounts(self) -> List[Account]:
    return self.session.query(Account).all()


class PasswordRepository:

  def __init__(self,
        token_factory,
        password_hasher,
        sqlalchemy_session: Session,
  ):
    self.token_factory = token_factory
    self.hasher = password_hasher
    self.session = sqlalchemy_session

  def add_password_reset_token(self, password_reset_token: PasswordResetToken):
    current_reset_token = self.session.query(PasswordResetToken). \
      filter_by(account_id=password_reset_token.account_id).first()
    if current_reset_token:
      current_reset_token.token = password_reset_token.token
    else:
      self.session.add(password_reset_token)
    self.session.commit()

  def find_password_reset_token_by_token(self, token):
    return self.session.query(PasswordResetToken). \
      filter(PasswordResetToken.token.like(token)).first()

  def update_password(self, account_id, password):
    salt_hashed_password = self.hasher.create_salt_hashed_password(password)
    salt = salt_hashed_password[0]
    hash = salt_hashed_password[1]
    hashed_password = self.session.query(HashedPassword). \
      filter(HashedPassword.account_id == account_id).first()
    hashed_password.salt = salt
    hashed_password.salted_hash = hash
    self.session.commit()

  def remove_password_reset_token(self, token):
    password_reset_token = self.session.query(PasswordResetToken). \
      filter(PasswordResetToken.token.like(token)).first()
    if password_reset_token:
      self.session.delete(password_reset_token)
      self.session.commit()

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
