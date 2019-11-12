import os
from base64 import b64encode
from datetime import timedelta, datetime
from typing import Union, Optional, Callable, Any, List

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from aveslog.v0.models import Account
from aveslog.v0.models import AccountRegistration
from aveslog.v0.models import PasswordResetToken
from aveslog.v0.models import RefreshToken
from aveslog.v0.birder import BirderRepository
from aveslog.v0.link import LinkFactory
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.mail import EmailAddress
from aveslog.v0.mail import MailDispatcher
from aveslog.v0.account import Username
from aveslog.v0.account import AccountFactory
from aveslog.v0.account import TokenFactory
from aveslog.v0.account import Credentials
from aveslog.v0.account import PasswordRepository
from aveslog.v0.account import PasswordHasher
from aveslog.v0.account import AccountRepository
from aveslog.v0.account import Password


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


class RefreshTokenRepository:

  def __init__(self, sqlalchemy_session: Session):
    self.session = sqlalchemy_session

  def put_refresh_token(self, token: RefreshToken) -> RefreshToken:
    if not token.id:
      return self.__insert_refresh_token(token)
    return self.__update_refresh_token(token)

  def refresh_token_by_jwt(self, jwt: str) -> Optional[RefreshToken]:
    return self.session.query(RefreshToken).filter_by(token=jwt).first()

  def remove_refresh_tokens(self, account: Account) -> List[RefreshToken]:
    refresh_tokens = self.session.query(RefreshToken).filter_by(
      account_id=account.id).all()
    for refresh_token in refresh_tokens:
      self.session.delete(refresh_token)
    self.session.commit()
    return refresh_tokens

  def refresh_token(self, refresh_token_id: int) -> Optional[RefreshToken]:
    return self.session.query(RefreshToken).get(refresh_token_id)

  def remove_refresh_token(self,
        refresh_token: RefreshToken) -> Optional[RefreshToken]:
    self.session.delete(refresh_token)
    self.session.commit()
    return refresh_token

  def __insert_refresh_token(self, token: RefreshToken) -> RefreshToken:
    self.session.add(token)
    self.session.commit()
    return token

  def __update_refresh_token(self, token: RefreshToken) -> RefreshToken:
    current = self.refresh_token(token.id)
    current.token = token.token
    current.account_id = token.account_id
    current.expiration_date = token.expiration_date
    self.session.commit()
    return current


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
        birder_repository: BirderRepository,
        token_factory: TokenFactory,
  ):
    self.account_factory = account_factory
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory
    self.birder_repository = birder_repository
    self.token_factory = token_factory

  def initiate_registration(
        self,
        raw_email: str,
        locale: LoadedLocale) -> Union[AccountRegistration, str]:
    if not EmailAddress.is_valid(raw_email):
      return 'email invalid'
    email = EmailAddress(raw_email)
    if self.account_repository.find_account_by_email(email):
      return 'email taken'
    token = self.token_factory.create_token()
    registration = AccountRegistration(email=email.raw, token=token)
    registration = self.account_repository.add_account_registration(
      registration)
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
      'Hi there, thanks for showing interest in aveslog. '
      'Here is your link to the registration form: ')
    return locale.text(message) + link

  def perform_registration(self,
        raw_email: str,
        registration_token: str,
        raw_username: str,
        raw_password: str,
  ) -> str:
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
    self.__initialize_account_birder(account)
    return 'success'

  def __remove_registration(self, registration_id: int) -> None:
    self.account_repository.remove_account_registration_by_id(registration_id)

  def __initialize_account_birder(self, account: Account) -> None:
    birder = self.birder_repository.add_birder(account.username)
    self.account_repository.set_account_birder(account, birder)


class PasswordUpdateController:

  def __init__(self,
        password_repository: PasswordRepository,
        refresh_token_repository: RefreshTokenRepository):
    self.password_repository = password_repository
    self.refresh_token_repository = refresh_token_repository

  def update_password(self, account: Account, password: Password) -> None:
    self.password_repository.update_password(account.id, password)
    self.refresh_token_repository.remove_refresh_tokens(account)


class PasswordResetController:

  def __init__(self,
        account_repository: AccountRepository,
        password_repository: PasswordRepository,
        link_factory: LinkFactory,
        mail_dispatcher: MailDispatcher,
        password_update_controller: PasswordUpdateController,
        token_factory: TokenFactory,
  ) -> None:
    self.account_repository = account_repository
    self.password_repository = password_repository
    self.link_factory = link_factory
    self.mail_dispatcher = mail_dispatcher
    self.password_update_controller = password_update_controller
    self.token_factory = token_factory

  def initiate_password_reset(
        self,
        raw_email: str,
        locale: LoadedLocale) -> bool:
    email = EmailAddress(raw_email)
    account = self.account_repository.find_account_by_email(email)
    if not account:
      return False
    token = self.token_factory.create_token()
    reset_token = PasswordResetToken(account_id=account.id, token=token)
    self.password_repository.add_password_reset_token(reset_token)
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
    reset_token = self.password_repository.find_password_reset_token_by_token(
      token)
    if not reset_token:
      return None
    account = self.account_repository.account_by_id(reset_token.account_id)
    self.password_update_controller.update_password(account, Password(password))
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
