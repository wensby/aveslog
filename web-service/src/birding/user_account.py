from hashlib import pbkdf2_hmac
from base64 import b64encode, b64decode
import binascii
import os
import re

username_regex = re.compile('^[A-Za-z0-9_.-]{5,32}$')
password_regex = re.compile('^.{8,128}$')

def is_valid_username(username):
  return username_regex.match(username)

def is_valid_password(password):
  return password_regex.match(password)

class UserAccount:

  def __init__(self, id, username, email, person_id, locale_id):
    self.id = id
    self.username = username
    self.email = email
    self.person_id = person_id
    self.locale_id = locale_id

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2], row[3], row[4])

class UserAccountRegistration:

  def __init__(self, id, email, token):
    self.id = id
    self.email = email
    self.token = token

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2])

class Credentials:

  def __init__(self, username, password):
    if not is_valid_username(username):
      raise Exception("invalid username format")
    if not is_valid_password(password):
      raise Exception("invalid password format")
    self.username = username
    self.password = password

  def is_valid(username, password):
    return is_valid_username(username) and is_valid_password(password)

class HashedPassword:

  def __init__(self, user_account_id, salt, salted_hash):
    self.user_account_id = user_account_id
    self.salt = salt
    self.salted_hash = salted_hash

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2])

class UserAccountRepository:

  def __init__(self, database, password_hasher):
    self.database = database
    self.hasher = password_hasher

  def remove_account_registration_by_id(self, id):
    query = ('DELETE FROM user_account_registration '
             'WHERE id = %s;')
    self.database.query(query, (id,))

  def create_account_registration(self, email):
    if not self.get_user_account_registration_by_email(email):
      token = os.urandom(16).hex()
      query = ('INSERT INTO user_account_registration (email, token) '
               'VALUES (%s, %s);')
      self.database.query(query, (email, token))
      return self.get_user_account_registration_by_email(email)

  def get_user_account_registration_by_email(self, email):
    query = ('SELECT id, email, token '
             'FROM user_account_registration '
             'WHERE email LIKE %s;')
    result = self.database.query(query, (email,))
    return next(map(UserAccountRegistration.fromrow, result.rows), None)

  def find_account_registration(self, email, token):
    query = ('SELECT id, email, token '
             'FROM user_account_registration '
             'WHERE email LIKE %s AND token LIKE %s;')
    result = self.database.query(query, (email, token))
    return next(map(UserAccountRegistration.fromrow, result.rows), None)

  def find_account_registration_by_token(self, token):
    query = ('SELECT id, email, token '
             'FROM user_account_registration '
             'WHERE token LIKE %s;')
    result = self.database.query(query, (token,))
    return next(map(UserAccountRegistration.fromrow, result.rows), None)

  def get_user_account_by_id(self, id):
    query = ('SELECT id, username, email, person_id, locale_id '
             'FROM user_account '
             'WHERE id = %s;')
    result = self.database.query(query, (id,))
    return next(map(UserAccount.fromrow, result.rows), None)

  def find_user_account(self, username):
    query = ('SELECT id, username, email, person_id, locale_id '
             'FROM user_account '
             'WHERE username LIKE %s;')
    result = self.database.query(query, (username,))
    return next(map(UserAccount.fromrow, result.rows), None)

  def find_account_by_email(self, email):
    query = ('SELECT id, username, email, person_id, locale_id '
             'FROM user_account '
             'WHERE email LIKE %s;')
    result = self.database.query(query, (email,))
    return next(map(UserAccount.fromrow, result.rows), None)

  def find_hashed_password(self, user_account):
    query = ('SELECT user_account_id, salt, salted_hash '
             'FROM hashed_password '
             'WHERE user_account_id = %s;')
    result = self.database.query(query, (user_account.id,))
    return next(map(HashedPassword.fromrow, result.rows), None)

  def put_new_user_account(self, email, username, password):
    if not Credentials.is_valid(username, password):
      return None
    if not self.find_user_account(username):
      query = ('INSERT INTO user_account (username, email) '
               'VALUES (%s, %s);')
      self.database.query(query, (username, email))
      account = self.find_user_account(username)
      if not account:
        return
      salt = b64encode(os.urandom(16)).decode('utf-8')
      hash = self.hasher.hash_password(password, salt)
      query = ('INSERT '
               'INTO hashed_password (user_account_id, salt, salted_hash) '
               'VALUES (%s, %s, %s);')
      self.database.query(query, (account.id, salt, hash))
      if self.find_hashed_password(account):
        return account

  def set_user_account_person(self, account, person):
    query = ('UPDATE user_account '
             'SET person_id = %s '
             'WHERE id = %s;')
    self.database.query(query, (person.id, account.id))

class PasswordHasher:

  def __init__(self, salt_factory):
    self.salt_factory = salt_factory

  def create_salt_hashed_password(self, password):
    salt = self.salt_factory.create_salt()
    hash = self.hash_password(password, salt)
    return (salt, hash)

  def hash_password(self, password, salt):
    encoded_password = password.encode()
    encoded_salt = salt.encode()
    binary_hash = pbkdf2_hmac('sha256', encoded_password, encoded_salt, 100000)
    return binascii.hexlify(binary_hash).decode()

class Authenticator:

  def __init__(self, user_account_repository, password_hasher):
    self.account_repository = user_account_repository
    self.hasher = password_hasher

  def is_account_password_correct(self, account, password):
    hashed_password = self.account_repository.find_hashed_password(account)
    if hashed_password:
      salt = hashed_password.salt
      expected_hash = hashed_password.salted_hash
      return self.hasher.hash_password(password, salt) == expected_hash

  def get_authenticated_user_account(self, credentials):
    username = credentials.username
    password = credentials.password
    account = self.account_repository.find_user_account(username)
    if account and self.is_account_password_correct(account, password):
      return account

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
    return ('PasswordResetToken<'
      f'user_account_id={self.user_account_id}, '
      f'token={self.token}'
      '>')

  def __eq__(self, other):
    if isinstance(other, PasswordResetToken):
      return self.__dict__ == other.__dict__
    return False

class TokenFactory:

  def create_token(self):
    return os.urandom(16).hex()
