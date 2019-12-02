from hashlib import pbkdf2_hmac
import binascii
import os
import re
from typing import Optional, Any, TypeVar

from flask import g
from aveslog.v0.models import Birder, Account, AccountRegistration, \
  HashedPassword, PasswordResetToken

from aveslog.mail import EmailAddress


def is_valid_username(username: str) -> bool:
  return re.compile('^[a-z0-9_.-]{5,32}$').match(username) is not None


def is_valid_password(password: str) -> bool:
  return re.compile('^.{8,128}$').match(password) is not None


class PasswordHasher:

  def __init__(self, salt_factory):
    self.salt_factory = salt_factory

  def create_salt_hashed_password(self, password):
    salt = self.salt_factory.create_salt()
    hash = self.hash_password(password, salt)
    return (salt, hash)

  def hash_password(self, password: str, salt: str) -> str:
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

  def __init__(self, password_hasher: PasswordHasher):
    self.hasher = password_hasher

  def add(self, account: Account) -> Account:
    g.database_session.add(account)
    g.database_session.commit()
    return account

  def account_by_id(self, account_id: int) -> Optional[Account]:
    return g.database_session.query(Account).get(account_id)

  def remove_account_registration_by_id(self, account_id: int) -> None:
    account_registration = g.database_session.query(AccountRegistration). \
      filter_by(id=account_id).first()
    g.database_session.delete(account_registration)
    g.database_session.commit()

  def add_account_registration(self,
        account_registration: AccountRegistration,
  ) -> Optional[AccountRegistration]:
    g.database_session.add(account_registration)
    g.database_session.commit()
    return account_registration

  def find_account_by_email(self, email: EmailAddress) -> Optional[Account]:
    return g.database_session.query(Account). \
      filter(Account.email.like(email.raw)).first()

  def find_hashed_password(self, account: Account) -> Optional[HashedPassword]:
    return g.database_session.query(HashedPassword).filter_by(
      account_id=account.id).first()

  def set_account_birder(self, account: Account, birder: Birder) -> None:
    account = g.database_session.query(Account).filter_by(id=account.id).first()
    account.birder_id = birder.id
    g.database_session.commit()


class PasswordRepository:

  def __init__(self, token_factory, password_hasher):
    self.token_factory = token_factory
    self.hasher = password_hasher

  def add_password_reset_token(self, password_reset_token: PasswordResetToken):
    current_reset_token = g.database_session.query(PasswordResetToken). \
      filter_by(account_id=password_reset_token.account_id).first()
    if current_reset_token:
      current_reset_token.token = password_reset_token.token
    else:
      g.database_session.add(password_reset_token)
    g.database_session.commit()

  def find_password_reset_token_by_token(self, token):
    return g.database_session.query(PasswordResetToken). \
      filter(PasswordResetToken.token.like(token)).first()

  def update_password(self, account_id, password):
    salt_hashed_password = self.hasher.create_salt_hashed_password(password)
    salt = salt_hashed_password[0]
    hash = salt_hashed_password[1]
    hashed_password = g.database_session.query(HashedPassword). \
      filter(HashedPassword.account_id == account_id).first()
    hashed_password.salt = salt
    hashed_password.salted_hash = hash
    g.database_session.commit()

  def remove_password_reset_token(self, token):
    password_reset_token = g.database_session.query(PasswordResetToken). \
      filter(PasswordResetToken.token.like(token)).first()
    if password_reset_token:
      g.database_session.delete(password_reset_token)
      g.database_session.commit()


class AccountFactory:

  def __init__(self, password_hasher: PasswordHasher):
    self.password_hasher = password_hasher
