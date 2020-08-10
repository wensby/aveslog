from datetime import datetime
from http import HTTPStatus

from flask import Response, make_response, jsonify, request, current_app, g

from aveslog.v0.link import LinkFactory
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
  session = g.database_session
  account = session.query(Account).filter_by(email=email).first()
  if not account:
    return error_response(
      ErrorCode.EMAIL_MISSING,
      'E-mail not associated with any account',
    )
  new_token = TokenFactory().create_token()
  previous_reset_token = account.password_reset_token
  if previous_reset_token:
    previous_reset_token.token = new_token
  else:
    session.add(PasswordResetToken(account_id=account.id, token=new_token))
  link_factory = LinkFactory(
    current_app.config['EXTERNAL_HOST'],
    current_app.config['FRONTEND_HOST'],
  )
  link = link_factory.create_frontend_link(
    f'/authentication/password-reset/{new_token}')
  message = (
    'You have requested a password reset of your Birding account. '
    'Please follow this link to get to your password reset form: ')
  locale = load_english_locale()
  mail_message = locale.text(message) + link
  g.mail_dispatcher.dispatch(email, 'Birding Password Reset', mail_message)
  session.commit()
  return make_response('', HTTPStatus.OK)


def post_password_reset(token: str) -> Response:
  password = request.json['password']
  session = g.database_session
  reset_token = session.query(PasswordResetToken).filter_by(token=token).first()
  if not reset_token:
    return make_response('', HTTPStatus.NOT_FOUND)
  account = reset_token.account
  password_hasher = PasswordHasher(SaltFactory())
  password_update_controller = PasswordUpdateController(password_hasher)
  password_update_controller.update_password(account, password, session)
  session.delete(reset_token)
  session.commit()
  return make_response('', HTTPStatus.OK)


def post_username_recovery() -> Response:
  email = request.json['email']
  session = g.database_session
  account = session.query(Account).filter_by(email=email).first()
  if not account:
    return error_response(
      ErrorCode.EMAIL_MISSING,
      'E-mail not associated with any account',
    )
  message = 'Your aveslog.com username is: ' + account.username
  g.mail_dispatcher.dispatch(email, 'Aveslog Username Recovery', message)
  session.commit()
  return make_response(jsonify({'email-status': 'sent'}), HTTPStatus.OK)


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
  loader = LocaleLoader(locales_directory_path)
  repository = LocaleRepository(locales_directory_path, loader)
  locale = repository.find_locale_by_code('en')
  return loader.load_locale(locale)
