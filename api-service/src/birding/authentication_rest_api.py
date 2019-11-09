from functools import wraps
from http import HTTPStatus
from typing import Optional, Callable
from typing import Union

from flask import Blueprint, Response
from flask import make_response
from flask import jsonify
from flask import request
from datetime import datetime

from .v0.localization import LocaleLoader
from .v0.localization import LoadedLocale
from .v0.localization import LocaleRepository
from .authentication import AuthenticationTokenFactory, Authenticator
from .authentication import AccessToken
from .authentication import PasswordUpdateController
from .authentication import RefreshTokenRepository
from .authentication import PasswordResetController
from .authentication import AccountRegistrationController
from .authentication import JwtDecoder
from .account import AccountRepository
from .account import Password
from .v0.models import Account, AccountRegistration, RefreshToken

RouteFunction = Callable[..., Response]


def create_unauthorized_response(message):
  data = jsonify({'status': 'failure', 'message': message})
  return make_response(data, HTTPStatus.UNAUTHORIZED)


def require_authentication(
      jwt_decoder: JwtDecoder,
      account_repository: AccountRepository) -> RouteFunction:
  """Wraps a route to require a valid authentication token

  The wrapped route will be provided with the authenticated account through a
  parameter named 'account'.
  """

  def route_decorator(route: RouteFunction) -> RouteFunction:
    @wraps(route)
    def route_wrapper(**kwargs):
      access_token = request.headers.get('accessToken')
      if not access_token:
        return authentication_token_missing_response()
      decode_result = jwt_decoder.decode_jwt(access_token)
      if not decode_result.ok:
        if decode_result.error == 'token-invalid':
          return create_unauthorized_response('authentication token invalid')
        elif decode_result.error == 'signature-expired':
          return create_unauthorized_response('authentication token expired')
      account_id = decode_result.payload['sub']
      account = account_repository.account_by_id(account_id)
      if not account:
        return create_unauthorized_response('account missing')
      return route(**kwargs, account=account)

    return route_wrapper

  return route_decorator


def authentication_token_missing_response() -> Response:
  return make_response(jsonify({
    'status': 'failure',
    'message': 'authentication token required',
  }), HTTPStatus.UNAUTHORIZED)


def create_authentication_rest_api_blueprint(
      account_repository: AccountRepository,
      authenticator: Authenticator,
      password_reset_controller: PasswordResetController,
      registration_controller: AccountRegistrationController,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
      jwt_decoder: JwtDecoder,
      password_update_controller: PasswordUpdateController,
      refresh_token_repository: RefreshTokenRepository,
      token_factory: AuthenticationTokenFactory) -> Blueprint:
  blueprint_name = 'authentication'
  url_prefix = '/authentication'
  blueprint = Blueprint(blueprint_name, __name__, url_prefix=url_prefix)

  @blueprint.route('/registration', methods=['POST'])
  def post_registration_email() -> Response:
    result = initiate_registration(request.json['email'])
    if result == 'email taken':
      return email_taken_response()
    elif result == 'email invalid':
      return email_invalid_response()
    return email_registration_success_response()

  @blueprint.route('/registration/<string:registration_token>')
  def get_registration(registration_token: str) -> Response:
    registration = find_registration_token(registration_token)
    if registration:
      return registration_response(registration)
    return make_response('', HTTPStatus.NOT_FOUND)

  @blueprint.route(
    '/registration/<string:registration_token>', methods=['POST'])
  def post_registration(registration_token: str) -> Response:
    username = request.json['username']
    password = request.json['password']
    response = try_perform_registration(registration_token, username, password)
    if response == 'success':
      return registration_success_response()
    elif response == 'username taken':
      return username_taken_response()

  @blueprint.route('/refresh-token', methods=['POST'])
  def post_refresh_token() -> Response:
    username = request.args.get('username')
    password = request.args.get('password')
    account = account_repository.find_account(username)
    if not account:
      return token_failure_response()
    if not authenticator.is_account_password_correct(account, password):
      return token_failure_response()
    refresh_token = create_persistent_refresh_token(account)
    return refresh_token_response(refresh_token)

  @blueprint.route('/access-token')
  def get_access_token() -> Response:
    refresh_token_jwt = request.headers.get('refreshToken')
    if not refresh_token_jwt:
      return create_unauthorized_response('refresh token required')
    decode_result = jwt_decoder.decode_jwt(refresh_token_jwt)
    if not decode_result.ok:
      if decode_result.error == 'token-invalid':
        return create_unauthorized_response('refresh token invalid')
      elif decode_result.error == 'signature-expired':
        return create_unauthorized_response('refresh token expired')
    if not refresh_token_repository.refresh_token_by_jwt(refresh_token_jwt):
      return create_unauthorized_response('refresh token revoked')
    account_id = decode_result.payload['sub']
    access_token = token_factory.create_access_token(account_id)
    return access_token_response(access_token)

  @blueprint.route('/password-reset', methods=['POST'])
  def post_password_reset_email() -> Response:
    email = request.json['email']
    created = initiate_password_reset(email)
    if not created:
      return password_reset_creation_failure_response()
    return password_reset_created_response()

  @blueprint.route(
    '/password-reset/<string:password_reset_token>', methods=['POST'])
  def post_password_reset(password_reset_token: str) -> Response:
    password = request.json['password']
    success = try_perform_password_reset(password, password_reset_token)
    if not success:
      return password_reset_failure_response()
    return password_reset_success_response()

  @blueprint.route('/password', methods=['POST'])
  @require_authentication(jwt_decoder, account_repository)
  def post_password_update(account: Account) -> Response:
    old_password = request.json['oldPassword']
    raw_new_password = request.json['newPassword']
    old_password_correct = is_password_correct(account, old_password)
    if not old_password_correct:
      return old_password_incorrect_response()
    if not Password.is_valid(raw_new_password):
      return new_password_invalid_response()
    new_password = Password(raw_new_password)
    password_update_controller.update_password(account, new_password)
    return password_update_success_response()

  @blueprint.route('/refresh-token/<int:refresh_token_id>', methods=['DELETE'])
  @require_authentication(jwt_decoder, account_repository)
  def delete_refresh_token(account: Account, refresh_token_id: int) -> Response:
    refresh_token = refresh_token_repository.refresh_token(refresh_token_id)
    if not refresh_token:
      return refresh_token_deleted_response()
    if refresh_token.account_id != account.id:
      return delete_refresh_token_unauthorized_response()
    refresh_token_repository.remove_refresh_token(refresh_token)
    return refresh_token_deleted_response()

  def password_reset_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'Password reset token not recognized',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def initiate_registration(email: str) -> Union[AccountRegistration, str]:
    locale = load_english_locale()
    return registration_controller.initiate_registration(email, locale)

  def email_taken_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'Email taken',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def email_invalid_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'Email invalid',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def email_registration_success_response() -> Response:
    return make_response(jsonify({
      'status': 'success',
    }), HTTPStatus.OK)

  def find_registration_token(
        registration_token: str) -> Optional[AccountRegistration]:
    return account_repository.find_account_registration_by_token(
      registration_token)

  def registration_response(registration) -> Response:
    return make_response(jsonify({
      'status': 'success',
      'result': {
        'registration': {
          'email': registration.email
        }
      },
    }), HTTPStatus.OK)

  def try_perform_registration(
        registration_token: str,
        username: str,
        password: str) -> str:
    registration = find_registration_token(registration_token)
    return registration_controller.perform_registration(
      registration.email, registration.token, username, password)

  def registration_success_response() -> Response:
    return make_response(jsonify({
      'status': 'success',
      'message': 'Registration successful',
    }), HTTPStatus.OK)

  def username_taken_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'username already taken',
    }), HTTPStatus.CONFLICT)

  def refresh_token_response(refresh_token: RefreshToken) -> Response:
    return make_response(jsonify({
      'id': refresh_token.id,
      'refreshToken': refresh_token.token,
      'expirationDate': refresh_token.expiration_date.isoformat(),
    }), HTTPStatus.OK)

  def access_token_response(access_token: AccessToken) -> Response:
    return make_response(jsonify({
      'jwt': access_token.jwt,
      'expiresIn': (access_token.expiration_date - datetime.now()).seconds,
    }), HTTPStatus.OK)

  def token_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'Try again'
    }), HTTPStatus.UNAUTHORIZED)

  def create_persistent_refresh_token(account):
    token = token_factory.create_refresh_token(account.id)
    return refresh_token_repository.put_refresh_token(token)

  def initiate_password_reset(email: str) -> bool:
    locale = load_english_locale()
    return password_reset_controller.initiate_password_reset(
      email, locale)

  def password_reset_creation_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'E-mail not associated with any account',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def password_reset_created_response() -> Response:
    return make_response(jsonify({
      'status': 'success',
      'message': 'Password reset link sent to e-mail',
    }), HTTPStatus.OK)

  def try_perform_password_reset(
        password: str, password_reset_token: str) -> str:
    return password_reset_controller.perform_password_reset(
      password_reset_token, password)

  def password_reset_success_response() -> Response:
    return make_response(jsonify({
      'status': 'success',
      'message': 'Password reset successfully',
    }), HTTPStatus.OK)

  def is_password_correct(account: Account, password: str) -> bool:
    return authenticator.is_account_password_correct(account, password)

  def old_password_incorrect_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'old password incorrect',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def new_password_invalid_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'new password invalid',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def password_update_success_response() -> Response:
    return make_response('', HTTPStatus.NO_CONTENT)

  def refresh_token_deleted_response() -> Response:
    return make_response('', HTTPStatus.NO_CONTENT)

  def delete_refresh_token_unauthorized_response() -> Response:
    return make_response('', HTTPStatus.UNAUTHORIZED)

  def load_english_locale() -> LoadedLocale:
    locale = locale_repository.find_locale_by_code('en')
    return locale_loader.load_locale(locale)

  return blueprint
