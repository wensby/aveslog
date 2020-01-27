from http import HTTPStatus

from flask import Response
from flask import g
from flask import request
from flask import make_response
from flask import jsonify

from aveslog.v0.error import ErrorCode
from aveslog.v0.authentication import SaltFactory
from aveslog.v0.authentication import PasswordUpdateController
from aveslog.v0.authentication import Authenticator
from aveslog.v0.rest_api import error_response
from aveslog.v0.rest_api import validation_failed_error_response
from aveslog.v0.rest_api import require_authentication
from aveslog.v0.account import is_valid_username
from aveslog.v0.account import PasswordHasher
from aveslog.v0.account import is_valid_password
from aveslog.v0.models import AccountRegistration, HashedPassword
from aveslog.v0.models import Account
from aveslog.v0.models import Birder


def create_account() -> Response:
  token = request.json.get('token')
  username = request.json.get('username')
  password = request.json.get('password')
  field_validation_errors = validate_fields(password, username)
  if field_validation_errors:
    return validation_failed_error_response(field_validation_errors)
  session = g.database_session
  registration = session.query(AccountRegistration) \
    .filter_by(token=token).first()
  if not registration:
    return registration_request_token_invalid_response()
  if session.query(Account).filter_by(username=username).first():
    return username_taken_response()
  account = Account(username=username, email=registration.email)
  account.hashed_password = create_hashed_password(password)
  account.birder = Birder(name=account.username)
  session.add(account)
  session.delete(registration)
  session.commit()
  json = jsonify(authenticated_account_representation(account))
  return make_response(json, HTTPStatus.CREATED)


def authenticated_account_representation(account):
  representation = account_representation(account)
  representation.update({
    'email': account.email,
  })
  return representation


def account_representation(account):
  return {
    'id': account.id,
    'username': account.username,
    'birder': {
      'id': account.birder.id,
      'name': account.birder.name,
    },
  }


def create_hashed_password(password: str) -> HashedPassword:
  salt_factory = SaltFactory()
  password_hasher = PasswordHasher(salt_factory)
  salt, hash = password_hasher.create_salt_hashed_password(password)
  return HashedPassword(salt=salt, salted_hash=hash)


def username_taken_response():
  return error_response(
    ErrorCode.USERNAME_TAKEN,
    'Username taken',
    status_code=HTTPStatus.CONFLICT,
  )


def registration_request_token_invalid_response():
  return error_response(
    ErrorCode.INVALID_ACCOUNT_REGISTRATION_TOKEN,
    'Registration request token invalid',
    status_code=HTTPStatus.BAD_REQUEST,
  )


def validate_fields(password, username):
  errors = []
  if not is_valid_username(username):
    errors.append({
      'code': ErrorCode.INVALID_USERNAME_FORMAT,
      'field': 'username',
      'message': 'Username need to adhere to format: ^[a-z0-9_.-]{5,32}$',
    })
  if not is_valid_password(password):
    errors.append({
      'code': ErrorCode.INVALID_PASSWORD_FORMAT,
      'field': 'password',
      'message': 'Password need to adhere to format: ^.{8,128}$'
    })
  return errors


@require_authentication
def get_account(username: str):
  session = g.database_session
  account = session.query(Account).filter_by(username=username).first()
  if not account:
    return make_response('', HTTPStatus.NOT_FOUND)
  json = jsonify(account_representation(account))
  return make_response(json, HTTPStatus.OK)


@require_authentication
def get_accounts() -> Response:
  accounts = g.database_session.query(Account).all()
  json = jsonify({'items': list(map(account_summary_representation, accounts))})
  return make_response(json, HTTPStatus.OK)


@require_authentication
def get_me() -> Response:
  account = g.authenticated_account
  json = jsonify(authenticated_account_representation(account))
  return make_response(json, HTTPStatus.OK)


@require_authentication
def post_password() -> Response:
  account = g.authenticated_account
  old_password = request.json['oldPassword']
  new_password = request.json['newPassword']
  password_hasher = PasswordHasher(SaltFactory())
  authenticator = Authenticator(password_hasher)
  old_password_correct = authenticator.is_account_password_correct(account,
    old_password)
  if not old_password_correct:
    return error_response(
      ErrorCode.OLD_PASSWORD_INCORRECT,
      'Old password incorrect',
      status_code=HTTPStatus.UNAUTHORIZED,
    )
  if not is_valid_password(new_password):
    return error_response(ErrorCode.PASSWORD_INVALID, 'New password invalid')
  password_update_controller = PasswordUpdateController(password_hasher)
  session = g.database_session
  password_update_controller.update_password(account, new_password, session)
  session.commit()
  return make_response('', HTTPStatus.NO_CONTENT)


def account_summary_representation(account: Account):
  return {
    'username': account.username,
    'birderId': account.birder_id
  }
