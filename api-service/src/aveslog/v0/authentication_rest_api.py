from http import HTTPStatus

from datetime import datetime

from aveslog.v0.error import ErrorCode
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.rest_api import RestApiResponse, error_response
from aveslog.v0.authentication import AuthenticationTokenFactory, Authenticator
from aveslog.v0.authentication import PasswordUpdateController
from aveslog.v0.authentication import RefreshTokenRepository
from aveslog.v0.authentication import PasswordResetController
from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.account import AccountRepository
from aveslog.v0.account import Password
from aveslog.v0.models import Account, RefreshToken


def credentials_incorrect_response() -> RestApiResponse:
  return error_response(
    ErrorCode.CREDENTIALS_INCORRECT,
    'Credentials incorrect',
    HTTPStatus.UNAUTHORIZED,
  )


def create_unauthorized_response(message) -> RestApiResponse:
  return RestApiResponse(HTTPStatus.UNAUTHORIZED, {
    'status': 'failure',
    'message': message,
  })


def refresh_token_deleted_response() -> RestApiResponse:
  return RestApiResponse(HTTPStatus.NO_CONTENT, {})


class AuthenticationRestApi:

  def __init__(self,
        locale_repository: LocaleRepository,
        locale_loader: LocaleLoader,
        account_repository: AccountRepository,
        authenticator: Authenticator,
        token_factory: AuthenticationTokenFactory,
        refresh_token_repository: RefreshTokenRepository,
        jwt_decoder: JwtDecoder,
        password_reset_controller: PasswordResetController,
        password_update_controller: PasswordUpdateController,
  ):
    self._locale_repository = locale_repository
    self._locale_loader = locale_loader
    self._account_repository = account_repository
    self._authenticator = authenticator
    self._token_factory = token_factory
    self._refresh_token_repository = refresh_token_repository
    self._jwt_decoder = jwt_decoder
    self._password_reset_controller = password_reset_controller
    self._password_update_controller = password_update_controller

  def post_refresh_token(self, username: str, password: str) -> RestApiResponse:
    account = self._account_repository.find_account(username)
    if not account:
      return credentials_incorrect_response()
    if not self._authenticator.is_account_password_correct(account, password):
      return credentials_incorrect_response()
    refresh_token = self._create_persistent_refresh_token(account)
    return RestApiResponse(HTTPStatus.CREATED, {
      'id': refresh_token.id,
      'refreshToken': refresh_token.token,
      'expirationDate': refresh_token.expiration_date.isoformat(),
    })

  def delete_refresh_token(self,
        account: Account,
        refresh_token_id: int,
  ) -> RestApiResponse:
    refresh_token = self._refresh_token_repository.refresh_token(
      refresh_token_id)
    if not refresh_token:
      return refresh_token_deleted_response()
    if refresh_token.account_id != account.id:
      return error_response(
        ErrorCode.AUTHORIZATION_REQUIRED,
        'Authorization required',
        HTTPStatus.UNAUTHORIZED,
      )
    self._refresh_token_repository.remove_refresh_token(refresh_token)
    return refresh_token_deleted_response()

  def get_access_token(self, refresh_token_jwt):
    if not refresh_token_jwt:
      return create_unauthorized_response('refresh token required')
    decode_result = self._jwt_decoder.decode_jwt(refresh_token_jwt)
    if not decode_result.ok:
      if decode_result.error == 'token-invalid':
        return create_unauthorized_response('refresh token invalid')
      elif decode_result.error == 'signature-expired':
        return create_unauthorized_response('refresh token expired')
    if not self._refresh_token_repository.refresh_token_by_jwt(
          refresh_token_jwt):
      return create_unauthorized_response('refresh token revoked')
    account_id = decode_result.payload['sub']
    access_token = self._token_factory.create_access_token(account_id)
    return RestApiResponse(HTTPStatus.OK, {
      'jwt': access_token.jwt,
      'expiresIn': (access_token.expiration_date - datetime.now()).seconds,
    })

  def post_password_reset_email(self, email) -> RestApiResponse:
    created = self._initiate_password_reset(email)
    if not created:
      return error_response(
        ErrorCode.EMAIL_MISSING,
        'E-mail not associated with any account',
      )
    return RestApiResponse(HTTPStatus.OK, {})

  def post_password_reset(self, password, token) -> RestApiResponse:
    success = self._try_perform_password_reset(password, token)
    if not success:
      return RestApiResponse(HTTPStatus.NOT_FOUND, {})
    return RestApiResponse(HTTPStatus.OK, {})

  def post_password(self,
        account: Account,
        old_password: str,
        raw_new_password: str,
  ) -> RestApiResponse:
    old_password_correct = self._is_password_correct(account, old_password)
    if not old_password_correct:
      return error_response(
        ErrorCode.OLD_PASSWORD_INCORRECT,
        'Old password incorrect',
        HTTPStatus.UNAUTHORIZED,
      )
    if not Password.is_valid(raw_new_password):
      return error_response(ErrorCode.PASSWORD_INVALID, 'New password invalid')
    new_password = Password(raw_new_password)
    self._password_update_controller.update_password(account, new_password)
    return RestApiResponse(HTTPStatus.NO_CONTENT, {})

  def _create_persistent_refresh_token(self, account: Account) -> RefreshToken:
    token = self._token_factory.create_refresh_token(account.id)
    return self._refresh_token_repository.put_refresh_token(token)

  def _initiate_password_reset(self, email: str) -> bool:
    locale = self._load_english_locale()
    return self._password_reset_controller.initiate_password_reset(
      email, locale)

  def _try_perform_password_reset(self,
        password: str, password_reset_token: str) -> str:
    return self._password_reset_controller.perform_password_reset(
      password_reset_token, password)

  def _is_password_correct(self, account: Account, password: str) -> bool:
    return self._authenticator.is_account_password_correct(account, password)

  def _load_english_locale(self) -> LoadedLocale:
    locale = self._locale_repository.find_locale_by_code('en')
    return self._locale_loader.load_locale(locale)
