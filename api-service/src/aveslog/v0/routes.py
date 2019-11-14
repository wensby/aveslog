from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import Response, request

from aveslog.v0.account import AccountRepository
from aveslog.v0.account_rest_api import AccountsRestApi
from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.authentication_rest_api import AuthenticationRestApi
from aveslog.v0.error import ErrorCode
from aveslog.v0.models import Account
from aveslog.v0.registration_rest_api import RegistrationRestApi
from aveslog.v0.rest_api import error_response
from aveslog.v0.search_api import SearchApi
from aveslog.v0.birds_rest_api import BirdsRestApi
from aveslog.v0.birds_rest_api import create_flask_response

RouteFunction = Callable[..., Response]


def authentication_token_missing_response() -> Response:
  return create_flask_response(error_response(
    ErrorCode.AUTHORIZATION_REQUIRED,
    'Authorization required',
    HTTPStatus.UNAUTHORIZED,
  ))


def authorized_account_missing_response() -> Response:
  return create_flask_response(error_response(
    ErrorCode.ACCOUNT_MISSING,
    'Authorized account gone',
    HTTPStatus.UNAUTHORIZED,
  ))


def access_token_invalid_response() -> Response:
  return create_flask_response(error_response(
    ErrorCode.ACCESS_TOKEN_INVALID,
    'Access token invalid',
    HTTPStatus.UNAUTHORIZED,
  ))


def access_token_expired_response() -> Response:
  return create_flask_response(error_response(
    ErrorCode.ACCESS_TOKEN_EXPIRED,
    'Access token expired',
    HTTPStatus.UNAUTHORIZED,
  ))


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
          return access_token_invalid_response()
        elif decode_result.error == 'signature-expired':
          return access_token_expired_response()
      account_id = decode_result.payload['sub']
      account = account_repository.account_by_id(account_id)
      if not account:
        return authorized_account_missing_response()
      return route(**kwargs, account=account)

    return route_wrapper

  return route_decorator


def create_birds_routes(birds_rest_api: BirdsRestApi):
  def get_bird(bird_identifier: str) -> Response:
    response = birds_rest_api.get_bird(bird_identifier)
    return create_flask_response(response)

  routes = [
    {
      'rule': '/birds/<string:bird_identifier>',
      'view_func': get_bird,
    },
  ]

  return routes


def create_search_routes(search_api: SearchApi):
  def search_birds() -> Response:
    query = request.args.get('q')
    page_size = request.args.get('page_size', type=int)
    embed = parse_embed_list(request.args)
    response = search_api.search_birds(query, embed, page_size)
    return create_flask_response(response)

  def parse_embed_list(args):
    return args.get('embed', type=str).split(',') if 'embed' in args else []

  return [
    {
      'rule': '/search/birds',
      'view_func': search_birds,
    }
  ]


def create_registration_routes(
      registration_rest_api: RegistrationRestApi,
) -> list:
  def post_registration_request() -> Response:
    email = request.json['email']
    response = registration_rest_api.create_registration_request(email)
    return create_flask_response(response)

  def get_registration_request(token: str) -> Response:
    response = registration_rest_api.get_registration_request(token)
    return create_flask_response(response)

  return [
    {
      'rule': '/registration-requests',
      'view_func': post_registration_request,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/registration-requests/<string:token>',
      'view_func': get_registration_request,
    },
  ]


def create_account_routes(
      jwt_decoder: JwtDecoder,
      account_repository: AccountRepository,
      accounts_rest_api: AccountsRestApi,
) -> list:
  def create_account() -> Response:
    response = accounts_rest_api.create_account(request.json)
    return create_flask_response(response)

  @require_authentication(jwt_decoder, account_repository)
  def get_accounts(account: Account) -> Response:
    response = accounts_rest_api.get_accounts()
    return create_flask_response(response)

  @require_authentication(jwt_decoder, account_repository)
  def get_me(account: Account) -> Response:
    response = accounts_rest_api.get_me(account)
    return create_flask_response(response)

  return [
    {
      'rule': '/accounts',
      'view_func': create_account,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/accounts',
      'view_func': get_accounts,
    },
    {
      'rule': '/account',
      'view_func': get_me,
    },
  ]


def create_authentication_routes(
      authentication_rest_api: AuthenticationRestApi,
      jwt_decoder: JwtDecoder,
      account_repository: AccountRepository,
) -> list:
  def post_registration(token: str) -> Response:
    username = request.json['username']
    password = request.json['password']
    response = authentication_rest_api.post_registration(
      token,
      username,
      password,
    )
    return create_flask_response(response)

  def post_refresh_token() -> Response:
    username = request.args.get('username')
    password = request.args.get('password')
    response = authentication_rest_api.post_refresh_token(username, password)
    return create_flask_response(response)

  @require_authentication(jwt_decoder, account_repository)
  def delete_refresh_token(account: Account, refresh_token_id: int) -> Response:
    response = authentication_rest_api.delete_refresh_token(
      account,
      refresh_token_id,
    )
    return create_flask_response(response)

  def get_access_token() -> Response:
    refresh_token_jwt = request.headers.get('refreshToken')
    response = authentication_rest_api.get_access_token(refresh_token_jwt)
    return create_flask_response(response)

  def post_password_reset_email() -> Response:
    email = request.json['email']
    response = authentication_rest_api.post_password_reset_email(email)
    return create_flask_response(response)

  def post_password_reset(token: str) -> Response:
    password = request.json['password']
    response = authentication_rest_api.post_password_reset(password, token)
    return create_flask_response(response)

  @require_authentication(jwt_decoder, account_repository)
  def post_password(account: Account) -> Response:
    old_password = request.json['oldPassword']
    raw_new_password = request.json['newPassword']
    response = authentication_rest_api.post_password(
      account,
      old_password,
      raw_new_password,
    )
    return create_flask_response(response)

  return [
    {
      'rule': '/authentication/registration/<string:token>',
      'view_func': post_registration,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/refresh-token',
      'view_func': post_refresh_token,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/refresh-token/<int:refresh_token_id>',
      'view_func': delete_refresh_token,
      'options': {'methods': ['DELETE']},
    },
    {
      'rule': '/authentication/access-token',
      'view_func': get_access_token,
    },
    {
      'rule': '/authentication/password-reset',
      'view_func': post_password_reset_email,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/password-reset/<string:token>',
      'view_func': post_password_reset,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/password',
      'view_func': post_password,
      'options': {'methods': ['POST']},
    },
  ]
