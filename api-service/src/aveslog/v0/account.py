from hashlib import pbkdf2_hmac
import binascii
import os
import re
from typing import Optional

from flask import g
from aveslog.v0.models import Account
from aveslog.v0.models import AccountRegistration
from aveslog.v0.models import PasswordResetToken

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
    return salt, hash

  def hash_password(self, password: str, salt: str) -> str:
    encoded_password = password.encode()
    encoded_salt = salt.encode()
    binary_hash = pbkdf2_hmac('sha256', encoded_password, encoded_salt, 100000)
    return binascii.hexlify(binary_hash).decode()


class TokenFactory:

  def create_token(self):
    return os.urandom(16).hex()


class AccountRepository:

  def __init__(self, password_hasher: PasswordHasher):
    self.hasher = password_hasher

  def add_account_registration(self,
        account_registration: AccountRegistration,
  ) -> Optional[AccountRegistration]:
    g.database_session.add(account_registration)
    g.database_session.commit()
    return account_registration

  def find_account_by_email(self, email: EmailAddress) -> Optional[Account]:
    return g.database_session.query(Account). \
      filter(Account.email.like(email.raw)).first()
