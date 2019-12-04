from datetime import datetime
from http import HTTPStatus
from typing import Optional

from flask import Response, make_response, jsonify, request, current_app, g

from aveslog.mail import EmailAddress
from aveslog.v0 import AccountRepository
from aveslog.v0 import LinkFactory
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.authentication import Authenticator
from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.authentication import PasswordUpdateController
from aveslog.v0.authentication import PasswordHasher
from aveslog.v0.authentication import SaltFactory
from aveslog.v0.authentication import TokenFactory
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.authentication import JwtFactory
from aveslog.v0.error import ErrorCode
from aveslog.v0.models import RefreshToken
from aveslog.v0.models import PasswordResetToken
from aveslog.v0.models import Account
from aveslog.v0.rest_api import error_response
from aveslog.v0.rest_api import require_authentication


def post_refresh_token() -> Response:
  username = request.args.get('username')
  password = request.args.get('password')
  session = g.database_session
  account = session.query(Account).filter_by(username=username).first()
  if not account:
    return credentials_incorrect_response()
  authenticator = Authenticator(PasswordHasher(SaltFactory()))
  if not authenticator.is_account_password_correct(account, password):
    return credentials_incorrect_response()
  session = g.database_session
  token_factory = AuthenticationTokenFactory(JwtFactory(current_app.secret_key),
    datetime.utcnow)
  refresh_token = token_factory.create_refresh_token(account.id)
  session.add(refresh_token)
  session.commit()
  return make_response(jsonify({
    'id': refresh_token.id,
    'refreshToken': refresh_token.token,
    'expirationDate': refresh_token.expiration_date.isoformat(),
  }), HTTPStatus.CREATED)


@require_authentication
def delete_refresh_token(refresh_token_id: int) -> Response:
  account = g.authenticated_account
  session = g.database_session
  refresh_token = session.query(RefreshToken).get(refresh_token_id)
  if not refresh_token:
    return refresh_token_deleted_response()
  if refresh_token.account_id != account.id:
    return error_response(
      ErrorCode.AUTHORIZATION_REQUIRED,
      'Authorization required',
      status_code=HTTPStatus.UNAUTHORIZED,
    )
  session.delete(refresh_token)
  session.commit()
  return refresh_token_deleted_response()


def get_access_token() -> Response:
  refresh_token_jwt = request.headers.get('refreshToken')
  if not refresh_token_jwt:
    return create_unauthorized_response('refresh token required')
  jwt_decoder = JwtDecoder(current_app.secret_key)
  decode_result = jwt_decoder.decode_jwt(refresh_token_jwt)
  if not decode_result.ok:
    if decode_result.error == 'token-invalid':
      return create_unauthorized_response('refresh token invalid')
    elif decode_result.error == 'signature-expired':
      return create_unauthorized_response('refresh token expired')
  token = g.database_session.query(RefreshToken) \
    .filter_by(token=refresh_token_jwt) \
    .first()
  if not token:
    return create_unauthorized_response('refresh token revoked')
  account_id = decode_result.payload['sub']
  token_factory = AuthenticationTokenFactory(JwtFactory(current_app.secret_key),
    datetime.utcnow)
  access_token = token_factory.create_access_token(account_id)
  return make_response(jsonify({
    'jwt': access_token.jwt,
    'expiresIn': (access_token.expiration_date - datetime.now()).seconds,
  }), HTTPStatus.OK)


def post_password_reset_email() -> Response:
  email = request.json['email']
  locale = load_english_locale()
  email = EmailAddress(email)
  account_repository = AccountRepository(PasswordHasher(SaltFactory()))
  account = account_repository.find_account_by_email(email)
  if not account:
    return error_response(
      ErrorCode.EMAIL_MISSING,
      'E-mail not associated with any account',
    )
  token = TokenFactory().create_token()
  reset_token = PasswordResetToken(account_id=account.id, token=token)
  g.database_session.add(reset_token)
  link = _create_password_reset_link(token)
  message = _create_mail_message(link, locale)
  g.mail_dispatcher.dispatch(email, 'Birding Password Reset', message)
  return make_response('', HTTPStatus.OK)


def post_password_reset(token: str) -> Response:
  password = request.json['password']
  success = try_perform_password_reset(password, token)
  if not success:
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response('', HTTPStatus.OK)


def credentials_incorrect_response() -> Response:
  return error_response(
    ErrorCode.CREDENTIALS_INCORRECT,
    'Credentials incorrect',
    status_code=HTTPStatus.UNAUTHORIZED,
  )


def create_unauthorized_response(message) -> Response:
  return make_response(jsonify({
    'status': 'failure',
    'message': message,
  }), HTTPStatus.UNAUTHORIZED)


def refresh_token_deleted_response() -> Response:
  return make_response('', HTTPStatus.NO_CONTENT)


def load_english_locale() -> LoadedLocale:
  locales_directory_path = current_app.config['LOCALES_PATH']
  loader = LocaleLoader(locales_directory_path, {})
  repository = LocaleRepository(locales_directory_path, loader)
  locale = repository.find_locale_by_code('en')
  return loader.load_locale(locale)


def _create_password_reset_link(token: str) -> str:
  link = f'/authentication/password-reset/{token}'
  return LinkFactory(current_app.config['EXTERNAL_HOST'],
    current_app.config['FRONTEND_HOST']).create_frontend_link(link)


def _create_mail_message(link: str, locale: LoadedLocale) -> str:
  message = (
    'You have requested a password reset of your Birding account. '
    'Please follow this link to get to your password reset form: ')
  return locale.text(message) + link


def try_perform_password_reset(password: str, token: str) -> Optional[str]:
  reset_token = g.database_session.query(PasswordResetToken). \
    filter(PasswordResetToken.token.like(token)).first()
  if not reset_token:
    return None
  account = g.database_session.query(Account).get(reset_token.account_id)
  password_update_controller = PasswordUpdateController(
    PasswordHasher(SaltFactory()))
  password_update_controller.update_password(account, password)
  password_reset_token = g.database_session.query(PasswordResetToken). \
    filter(PasswordResetToken.token.like(token)).first()
  if password_reset_token:
    g.database_session.delete(password_reset_token)
    g.database_session.commit()
  return 'success'
