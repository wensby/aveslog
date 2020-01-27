from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import Response, make_response, jsonify, request, current_app, g
from sqlalchemy import text

from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.error import ErrorCode
from aveslog.v0.models import Account
from aveslog.v0.models import Role
from aveslog.v0.models import ResourcePermission

RouteFunction = Callable[..., Response]


def error_response(
      error_code: int,
      message: str,
      additional_errors: list = None,
      status_code: int = HTTPStatus.BAD_REQUEST,
) -> Response:
  data = {
    'code': error_code,
    'message': message,
  }
  if additional_errors:
    data['errors'] = additional_errors
  return make_response(jsonify(data), status_code)


def validation_failed_error_response(field_validation_errors):
  return error_response(
    ErrorCode.VALIDATION_FAILED,
    'Validation failed',
    additional_errors=field_validation_errors,
  )


def cache(max_age=300) -> RouteFunction:
  def decorator(route):
    @wraps(route)
    def route_wrapper(**kwargs):
      response = route(**kwargs)
      response.headers['Cache-Control'] = f'max-age={max_age}'
      return response

    return route_wrapper

  return decorator


def require_authentication(route) -> RouteFunction:
  """Wraps a route to require a valid authentication token

  The wrapped route will then be able to access the authenticated account
  through g.authenticated_account.
  """

  @wraps(route)
  def route_wrapper(**kwargs):
    access_token = request.headers.get('accessToken')
    if not access_token:
      return authentication_token_missing_response()
    jwt_decoder = JwtDecoder(current_app.secret_key)
    decode_result = jwt_decoder.decode_jwt(access_token)
    if not decode_result.ok:
      if decode_result.error == 'token-invalid':
        return access_token_invalid_response()
      elif decode_result.error == 'signature-expired':
        return access_token_expired_response()
    account_id = decode_result.payload['sub']
    account = g.database_session.query(Account).get(account_id)
    if not account:
      return authorized_account_missing_response()
    g.authenticated_account = account
    return route(**kwargs)

  return route_wrapper


def require_permission(route) -> RouteFunction:
  """Wraps a route to requiring an authentication with necessary permissions"""

  @wraps(route)
  def route_wrapper(**kwargs):
    account: Account = g.authenticated_account
    matching_permissions = g.database_session.query(ResourcePermission) \
      .join(ResourcePermission.roles) \
      .filter(Role.accounts.any(id=account.id)) \
      .filter(text(":resource ~ resource_regex")) \
      .params(resource=request.path) \
      .filter(ResourcePermission.method == request.method) \
      .all()
    if not matching_permissions:
      return unauthorized_response()
    return route(**kwargs)

  return route_wrapper


def authentication_token_missing_response() -> Response:
  return error_response(
    ErrorCode.AUTHORIZATION_REQUIRED,
    'Authorization required',
    status_code=HTTPStatus.UNAUTHORIZED,
  )


def authorized_account_missing_response() -> Response:
  return error_response(
    ErrorCode.ACCOUNT_MISSING,
    'Authorized account gone',
    status_code=HTTPStatus.UNAUTHORIZED,
  )


def access_token_invalid_response() -> Response:
  return error_response(
    ErrorCode.ACCESS_TOKEN_INVALID,
    'Access token invalid',
    status_code=HTTPStatus.UNAUTHORIZED,
  )


def access_token_expired_response() -> Response:
  return error_response(
    ErrorCode.ACCESS_TOKEN_EXPIRED,
    'Access token expired',
    status_code=HTTPStatus.UNAUTHORIZED,
  )


def unauthorized_response() -> Response:
  return error_response(
    ErrorCode.AUTHORIZATION_REQUIRED,
    'Authorization required',
    status_code=HTTPStatus.UNAUTHORIZED,
  )
