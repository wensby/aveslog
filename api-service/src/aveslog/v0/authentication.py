import os
from base64 import b64encode
from datetime import timedelta, datetime
from typing import Union, Callable, Any

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from aveslog.v0.models import Account
from aveslog.v0.models import RegistrationRequest
from aveslog.v0.models import RefreshToken
from aveslog.v0.link import LinkFactory
from aveslog.v0.localization import LoadedLocale
from aveslog.mail import is_valid_email_address
from aveslog.mail import MailDispatcher
from aveslog.v0.account import TokenFactory
from aveslog.v0.account import PasswordHasher
from aveslog.v0.account import AccountRepository


class AccessToken:

  def __init__(self, jwt: str, account_id: int, expiration_date: datetime):
    self.jwt = jwt
    self.account_id = account_id
    self.expiration_date = expiration_date

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    return False

  def __hash__(self) -> int:
    return hash((self.jwt, self.account_id, self.expiration_date))

  def __repr__(self) -> str:
    return (f'{self.__class__.__name__}({self.jwt}, {self.account_id}, '
            f'{self.expiration_date})')


class Authenticator:

  def __init__(self, password_hasher: PasswordHasher) -> None:
    self.hasher = password_hasher

  def is_account_password_correct(self,
        account: Account,
        password: str) -> bool:
    hashed_password = account.hashed_password
    if not hashed_password:
      return False
    salt = hashed_password.salt
    expected_hash = hashed_password.salted_hash
    if self.hasher.hash_password(password, salt) != expected_hash:
      return False
    return True


class AccountRegistrationController:

  def __init__(self,
        account_repository: AccountRepository,
        mail_dispatcher: MailDispatcher,
        link_factory: LinkFactory,
        token_factory: TokenFactory,
  ):
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory
    self.token_factory = token_factory

  def initiate_registration(
        self,
        email: str,
        locale: LoadedLocale) -> Union[RegistrationRequest, str]:
    if not is_valid_email_address(email):
      return 'email invalid'
    if self.account_repository.find_account_by_email(email):
      return 'email taken'
    token = self.token_factory.create_token()
    registration_request = RegistrationRequest(email=email, token=token)
    registration_request = self.account_repository.add_account_registration(
      registration_request)
    self.__send_registration_email(email, registration_request, locale)
    return registration_request

  def __send_registration_email(self,
        email_address: str,
        registration_request: RegistrationRequest,
        locale: LoadedLocale) -> None:
    link = self.__create_registration_link(registration_request.token)
    self.__dispatch_registration_mail(email_address, link, locale)

  def __dispatch_registration_mail(self,
        email_address: str,
        registration_link: str,
        locale: LoadedLocale) -> None:
    subject = locale.text('Aveslog Registration')
    message = self.__create_registration_mail_message(registration_link, locale)
    self.mail_dispatcher.dispatch(email_address, subject, message)

  def __create_registration_link(self, token: str) -> str:
    link = f'/authentication/registration/{token}'
    return self.link_factory.create_frontend_link(link)

  def __create_registration_mail_message(self,
        link: str,
        locale: LoadedLocale) -> str:
    message = (
      'Hi there, thanks for showing interest in Aveslog. '
      'Here is your link to the registration form: ')
    return locale.text(message) + link


class PasswordUpdateController:

  def __init__(self, password_hasher: PasswordHasher):
    self._password_hasher = password_hasher

  def update_password(self, account: Account, password: str, session: Session):
    salt, hash = self._password_hasher.create_salt_hashed_password(password)
    hashed_password = account.hashed_password
    hashed_password.salt = salt
    hashed_password.salted_hash = hash
    for refresh_token in account.refresh_tokens:
      session.delete(refresh_token)
    session.flush()


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
    return encode(payload, self.secret, algorithm='HS256').decode('utf-8')


class AuthenticationTokenFactory:

  def __init__(self, jwt_factory: JwtFactory, time_supplier: TimeSupplier):
    self.jwt_factory = jwt_factory
    self.time_supplier = time_supplier

  def create_access_token(self,
        account_id: int,
        expiration: timedelta = timedelta(days=0, minutes=30)) -> AccessToken:
    time = self.time_supplier()
    expiration_date = time + expiration
    jwt = self.jwt_factory.create_token(account_id, time, expiration_date)
    return AccessToken(jwt, account_id, expiration_date)

  def create_refresh_token(self, account_id: int) -> RefreshToken:
    time = self.time_supplier()
    expiration_date = time + timedelta(days=90)
    jwt_token = self.jwt_factory.create_token(account_id, time, expiration_date)
    return RefreshToken(
      token=jwt_token, account_id=account_id, expiration_date=expiration_date)


class DecodeResult:

  def __init__(self, payload: dict, error: str = None) -> None:
    self.ok = not error
    self.error = error
    self.payload = payload


class JwtDecoder:

  def __init__(self, secret: str):
    self.secret = secret

  def decode_jwt(self, jwt: str) -> DecodeResult:
    try:
      payload = decode(jwt, self.secret, algorithms=['HS256'])
      return DecodeResult(payload)
    except ExpiredSignatureError:
      return DecodeResult({}, error='signature-expired')
    except InvalidTokenError:
      return DecodeResult({}, error='token-invalid')
