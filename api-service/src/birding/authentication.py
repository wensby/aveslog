import os
from base64 import b64encode
from datetime import timedelta, datetime
from typing import Union, Optional, Callable, Any, TypeVar, Type

import jwt

from .database import Database
from .database import read_script_file
from .person import PersonRepository
from .link import LinkFactory
from .localization import LoadedLocale
from .mail import EmailAddress
from .mail import MailDispatcher
from .account import Username, AccountFactory
from .account import Credentials
from .account import PasswordRepository
from .account import Account
from .account import PasswordHasher
from .account import AccountRepository
from .account import AccountRegistration
from .account import Password

RefreshTokenType = TypeVar('RefreshTokenType', bound='RefreshToken')


class RefreshToken:

  @classmethod
  def from_row(cls: Type[RefreshTokenType], row: list) -> RefreshTokenType:
    return cls(row[0], row[1], row[2], row[3])

  def __init__(self,
        refresh_token_id: Optional[int],
        jwt_token: str,
        account_id: int,
        expiration_date: datetime) -> None:
    self.id = refresh_token_id
    self.jwt_token = jwt_token
    self.account_id = account_id
    self.expiration_date = expiration_date

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, RefreshToken):
      return False
    return self.__dict__ == other.__dict__


class RefreshTokenRepository:

  def __init__(self, database: Database):
    self.database = database

  def refresh_token_by_jwt(self, jwt_token: str) -> Optional[RefreshToken]:
    with self.database.transaction() as transaction:
      query = read_script_file('select_refresh_token_by_jwt_token.sql')
      result = transaction.execute(query, (jwt_token,), RefreshToken.from_row)
      if not result.rows:
        return None
      else:
        return result.rows[0]

  def put_refresh_token(self, token: RefreshToken) -> RefreshToken:
    if not token.id:
      return self.__insert_refresh_token(token)
    return self.__update_refresh_token(token)

  def __insert_refresh_token(self, token: RefreshToken) -> RefreshToken:
    query = read_script_file('insert-refresh-token.sql')
    return self.__query_token(query, token)

  def __update_refresh_token(self, token: RefreshToken) -> RefreshToken:
    query = read_script_file('update-refresh-token.sql')
    return self.__query_token(query, token)

  def __query_token(self, query: str, token: RefreshToken) -> RefreshToken:
    with self.database.transaction() as transaction:
      values = {
        'id': token.id,
        'token': token.jwt_token,
        'account_id': token.account_id,
        'expiration_date': token.expiration_date,
      }
      return transaction.execute(query, values, RefreshToken.from_row).rows[0]


class Authenticator:

  def __init__(self,
        account_repository: AccountRepository,
        password_hasher: PasswordHasher) -> None:
    self.account_repository = account_repository
    self.hasher = password_hasher

  def is_account_password_correct(self,
        account: Account,
        password: Union[Password, str]) -> bool:
    hashed_password = self.account_repository.find_hashed_password(account)
    if not hashed_password:
      return False
    salt = hashed_password.salt
    expected_hash = hashed_password.salted_hash
    if self.hasher.hash_password(password, salt) != expected_hash:
      return False
    return True


class AccountRegistrationController:

  def __init__(self,
        account_factory: AccountFactory,
        account_repository: AccountRepository,
        mail_dispatcher: MailDispatcher,
        link_factory: LinkFactory,
        person_repository: PersonRepository) -> None:
    self.account_factory = account_factory
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory
    self.person_repository = person_repository

  def initiate_registration(
        self,
        raw_email: str,
        locale: LoadedLocale) -> Union[AccountRegistration, str]:
    if not EmailAddress.is_valid(raw_email):
      return 'email invalid'
    email = EmailAddress(raw_email)
    if self.account_repository.find_account_by_email(email):
      return 'email taken'
    registration = self.account_repository.create_account_registration(email)
    self.__send_registration_email(email, registration, locale)
    return registration

  def __send_registration_email(self,
        email_address: EmailAddress,
        registration: AccountRegistration,
        locale: LoadedLocale) -> None:
    link = self.__create_registration_link(registration.token)
    self.__dispatch_registration_mail(email_address, link, locale)

  def __dispatch_registration_mail(self,
        email_address: EmailAddress,
        registration_link: str,
        locale: LoadedLocale) -> None:
    subject = 'Birding Registration'
    message = self.__create_registration_mail_message(registration_link, locale)
    self.mail_dispatcher.dispatch(email_address, subject, message)

  def __create_registration_link(self, token: str) -> str:
    link = f'/authentication/registration/{token}'
    return self.link_factory.create_frontend_link(link)

  def __create_registration_mail_message(self,
        link: str,
        locale: LoadedLocale) -> str:
    message = (
      'Hi there, thanks for showing interest in birding. '
      'Here is your link to the registration form: ')
    return locale.text(message) + link

  def perform_registration(self,
        raw_email: str,
        registration_token: str,
        raw_username: str,
        raw_password: str) -> str:
    email = EmailAddress(raw_email)
    registration = self.account_repository.find_account_registration(
      email, registration_token)
    if not registration:
      return 'associated registration missing'
    username = Username(raw_username)
    if self.account_repository.find_account(username):
      return 'username taken'
    password = Password(raw_password)
    credentials = Credentials(username, password)
    account = self.account_factory.create_account(email, credentials)
    self.__remove_registration(registration.id)
    self.__initialize_account_person(account)
    return 'success'

  def __remove_registration(self, registration_id: int) -> None:
    self.account_repository.remove_account_registration_by_id(registration_id)

  def __initialize_account_person(self, account: Account) -> None:
    person = self.person_repository.add_person(account.username)
    self.account_repository.set_account_person(account, person)


class PasswordResetController:

  def __init__(self,
        account_repository: AccountRepository,
        password_repository: PasswordRepository,
        link_factory: LinkFactory,
        mail_dispatcher: MailDispatcher) -> None:
    self.account_repository = account_repository
    self.password_repository = password_repository
    self.link_factory = link_factory
    self.mail_dispatcher = mail_dispatcher

  def initiate_password_reset(
        self,
        raw_email: str,
        locale: LoadedLocale) -> bool:
    email = EmailAddress(raw_email)
    account = self.account_repository.find_account_by_email(email)
    if not account:
      return False
    token = self.password_repository.create_password_reset_token(account).token
    link = self.__create_password_reset_link(token)
    message = self.__create_mail_message(link, locale)
    self.mail_dispatcher.dispatch(email, 'Birding Password Reset', message)
    return True

  def __create_password_reset_link(self, token: str) -> str:
    link = f'/authentication/password-reset/{token}'
    return self.link_factory.create_frontend_link(link)

  def __create_mail_message(self, link: str, locale: LoadedLocale) -> str:
    message = (
      'You have requested a password reset of your Birding account. '
      'Please follow this link to get to your password reset form: ')
    return locale.text(message) + link

  def perform_password_reset(self, token: str, password: str) -> Optional[str]:
    account_id = self.password_repository.find_password_reset_account_id(token)
    if not account_id:
      return None
    self.password_repository.update_password(account_id, Password(password))
    self.password_repository.remove_password_reset_token(token)
    return 'success'


class SaltFactory:

  def create_salt(self) -> str:
    return b64encode(os.urandom(16)).decode('utf-8')


TimeSupplier = Callable[[], datetime]


class JwtFactory:

  def __init__(self, secret: str):
    self.secret = secret

  def create_token(self,
        subject_claim: Any,
        issue_date: datetime,
        expiration_date: datetime,
  ) -> str:
    payload = {
      'exp': expiration_date,
      'iat': issue_date,
      'sub': subject_claim
    }
    return jwt.encode(payload, self.secret, algorithm='HS256').decode('utf-8')


class AuthenticationTokenFactory:

  def __init__(self, jwt_factory: JwtFactory, time_supplier: TimeSupplier):
    self.jwt_factory = jwt_factory
    self.time_supplier = time_supplier

  def create_access_token(self,
        account_id: int,
        expiration: timedelta = timedelta(days=0, minutes=30)) -> str:
    time = self.time_supplier()
    expiration_date = time + expiration
    return self.jwt_factory.create_token(account_id, time, expiration_date)

  def create_refresh_token(self, account_id: int) -> RefreshToken:
    time = self.time_supplier()
    expiration_date = time + timedelta(days=90)
    jwt_token = self.jwt_factory.create_token(account_id, time, expiration_date)
    return RefreshToken(None, jwt_token, account_id, expiration_date)


class DecodeResult:

  def __init__(self, payload: dict, error: str = None) -> None:
    self.ok = not error
    self.error = error
    self.payload = payload


class AuthenticationTokenDecoder:

  def __init__(self, secret: str):
    self.secret = secret

  def decode_authentication_token(self, token: str) -> DecodeResult:
    try:
      payload = jwt.decode(token, self.secret, algorithms=['HS256'])
      return DecodeResult(payload)
    except jwt.ExpiredSignatureError:
      return DecodeResult({}, error='signature-expired')
    except jwt.InvalidTokenError:
      return DecodeResult({}, error='token-invalid')
