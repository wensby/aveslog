import datetime
import os
from base64 import b64encode
from datetime import timedelta

import jwt

from .mail import EmailAddress
from .account import Username, AccountFactory
from .account import Password

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
    password = credentials.password
    account = self.account_repository.find_user_account(credentials.username)
    if account and self.is_account_password_correct(account, password):
      return account

class AccountRegistrationController:

  def __init__(self, account_factory: AccountFactory, account_repository, mail_dispatcher, link_factory, person_repository):
    self.account_factory = account_factory
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory
    self.person_repository = person_repository

  def initiate_registration(self, raw_email, locale):
    if not EmailAddress.is_valid(raw_email):
      return 'email invalid'
    email = EmailAddress(raw_email)
    if self.account_repository.find_account_by_email(email):
      return 'email taken'
    registration = self.account_repository.create_account_registration(email)
    self.__send_registration_email(email, registration, locale)
    return registration

  def __send_registration_email(self, email_address, registration, locale):
    token = registration.token
    link = self.link_factory.create_endpoint_external_link('authentication.get_register_form', token=token)
    message = self.create_registration_mail_message(link, locale)
    self.mail_dispatcher.dispatch(email_address, 'Birding Registration', message)

  def create_registration_mail_message(self, link, locale):
    message = (
        'Hi there, thanks for showing interest in birding. '
        'Here is your link to the registration form: ')
    return locale.text(message) + link

  def perform_registration(self, raw_email, registration_token, raw_username, raw_password):
    email = EmailAddress(raw_email)
    registration = self.__find_associated_registration(email, registration_token)
    if not registration:
      return 'associated registration missing'
    username = Username(raw_username)
    if self.account_repository.find_user_account(username):
      return 'username taken'
    password = Password(raw_password)
    account = self.account_factory.create_account(email, username, password)
    self.__remove_registration(registration.id)
    self.__initialize_account_person(account)
    return 'success'

  def __find_associated_registration(self, email, token):
    return self.account_repository.find_account_registration(email, token)

  def __remove_registration(self, registration_id):
    self.account_repository.remove_account_registration_by_id(registration_id)

  def __initialize_account_person(self, account):
    person = self.person_repository.add_person(account.username)
    self.account_repository.set_user_account_person(account, person)

class PasswordResetController:

  def __init__(self, account_repository, password_repository, link_factory, mail_dispatcher):
    self.account_repository = account_repository
    self.password_repository = password_repository
    self.link_factory = link_factory
    self.mail_dispatcher = mail_dispatcher

  def initiate_password_reset(self, raw_email, locale, is_rest=False):
    email = EmailAddress(raw_email)
    account = self.account_repository.find_account_by_email(email)
    if not account:
      return False
    password_reset_token = self.password_repository.create_password_reset_token(account)
    token = password_reset_token.token
    if is_rest:
      link = self.link_factory.create_frontend_link(f'/authentication/password-reset/{token}')
    else:
      link = self.link_factory.create_endpoint_external_link('authentication.get_password_reset_form', token=token)
    message = self.__create_mail_message(link, locale)
    self.mail_dispatcher.dispatch(email, 'Birding Password Reset', message)
    return True

  def __create_mail_message(self, link, locale):
    message = (
        'You have requested a password reset of your Birding account. '
        'Please follow this link to get to your password reset form: ')
    return locale.text(message) + link

  def perform_password_reset(self, token, password):
    account_id = self.password_repository.find_password_reset_account_id(token)
    if account_id:
      self.password_repository.update_password(account_id, Password(password))
      self.password_repository.remove_password_reset_token(token)
      return 'success'

class SaltFactory:

  def create_salt(self):
    return b64encode(os.urandom(16)).decode('utf-8')

class AuthenticationTokenFactory:

  def __init__(self, secret, utc_now_supplier):
    self.secret = secret
    self.utc_now_supplier = utc_now_supplier

  def create_authentication_token(self,
        account_id: int,
        expiration: timedelta=timedelta(days=0, seconds=5)
  ) -> str:
    payload = {
      'exp': self.utc_now_supplier() + expiration,
      'iat': self.utc_now_supplier(),
      'sub': account_id
    }
    return jwt.encode(payload, self.secret, algorithm='HS256').decode('utf-8')

class DecodeResult:

  def __init__(self, payload: dict, error: str=None):
    self.ok = not error
    self.error = error
    self.payload = payload

class AuthenticationTokenDecoder:

  def __init__(self, secret):
    self.secret = secret

  def decode_authentication_token(self, token: str) -> DecodeResult:
    try:
      payload = jwt.decode(token, self.secret, algorithms=['HS256'])
      return DecodeResult(payload)
    except jwt.ExpiredSignatureError:
      return DecodeResult({}, error='signature-expired')
    except jwt.InvalidTokenError:
      return DecodeResult({}, error='token-invalid')
