from http import HTTPStatus
from typing import Optional
from typing import Union

from flask import Blueprint, Response
from flask import make_response
from flask import jsonify
from flask import request

from .localization import LocaleLoader
from .localization import LoadedLocale
from .localization import LocaleRepository
from .authentication import AuthenticationTokenFactory, Authenticator
from .authentication import PasswordResetController
from .authentication import AccountRegistrationController
from .account import AccountRepository
from .account import AccountRegistration


def create_authentication_rest_api_blueprint(
      account_repository: AccountRepository,
      authenticator: Authenticator,
      password_reset_controller: PasswordResetController,
      registration_controller: AccountRegistrationController,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
      token_factory: AuthenticationTokenFactory) -> Blueprint:
  blueprint_name = 'v2authentication'
  url_prefix = '/v2/authentication'
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

  @blueprint.route('/token')
  def get_token() -> Response:
    username = request.args.get('username')
    password = request.args.get('password')
    account = account_repository.find_user_account(username)
    if not account:
      return token_failure_response()
    if not authenticator.is_account_password_correct(account, password):
      return token_failure_response()
    token = token_factory.create_authentication_token(account.id)
    return token_response(token)

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
      'message': 'Username already taken',
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

  def token_response(token: str) -> Response:
    return make_response(jsonify({
      'status': 'success',
      'message': 'Successfully logged in.',
      'authToken': token
    }), HTTPStatus.OK)

  def token_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'Try again'
    }), HTTPStatus.INTERNAL_SERVER_ERROR)

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

  def load_english_locale() -> LoadedLocale:
    locale = locale_repository.find_locale_by_code('en')
    return locale_loader.load_locale(locale)

  return blueprint
