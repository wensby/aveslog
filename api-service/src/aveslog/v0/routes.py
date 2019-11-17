import os
from functools import wraps
from http import HTTPStatus
from typing import Callable, Union, Optional

from flask import Response, request

from aveslog.v0.localization import LoadedLocale, LocaleRepository, LocaleLoader
from aveslog.v0.link import LinkFactory
from aveslog.v0.bird import BirdRepository
from aveslog.v0.account import AccountRepository
from aveslog.v0.authentication import JwtDecoder, AccountRegistrationController
from aveslog.v0.authentication_rest_api import AuthenticationRestApi
from aveslog.v0.error import ErrorCode
from aveslog.v0.models import Account, Bird, Picture, AccountRegistration
from aveslog.v0.rest_api import error_response, RestApiResponse
from aveslog.v0.search_api import SearchApi
from aveslog.v0 import create_flask_response

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


def create_birds_routes(
      bird_repository: BirdRepository,
      link_factory: LinkFactory,
):
  def external_picture_url(picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return link_factory.create_url_external_link(static_picture_url)

  def get_bird_data(bird: Bird) -> dict:
    bird_data = {
      'id': bird.binomial_name.lower().replace(' ', '-'),
      'binomialName': bird.binomial_name,
    }
    if bird.thumbnail:
      bird_data['thumbnail'] = {
        'url': external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit,
      }
    if bird.thumbnail:
      bird_data['cover'] = {
        'url': external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit,
      }
    return bird_data

  def get_bird(bird_identifier: str) -> Response:
    if not isinstance(bird_identifier, str):
      raise Exception(f'Unexpected bird identifier: {bird_identifier}')
    reformatted = bird_identifier.replace('-', ' ')
    bird = bird_repository.get_bird_by_binomial_name(reformatted)
    if not bird:
      return create_flask_response(
        RestApiResponse(HTTPStatus.NOT_FOUND, {'message': 'Not Found'}))
    bird_data = get_bird_data(bird)
    return create_flask_response(RestApiResponse(HTTPStatus.OK, bird_data))

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
      registration_controller: AccountRegistrationController,
      account_repository: AccountRepository,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
) -> list:
  def find_registration_token(registration_token: str) -> Optional[
    AccountRegistration]:
    return account_repository.find_account_registration_by_token(
      registration_token)

  def load_english_locale() -> LoadedLocale:
    locale = locale_repository.find_locale_by_code('en')
    return locale_loader.load_locale(locale)

  def initiate_registration(email: str) -> Union[AccountRegistration, str]:
    locale = load_english_locale()
    return registration_controller.initiate_registration(email, locale)

  def post_registration_request() -> Response:
    email = request.json['email']
    result = initiate_registration(email)
    if result == 'email taken':
      return create_flask_response(
        error_response(ErrorCode.EMAIL_TAKEN, 'Email taken'))
    elif result == 'email invalid':
      return create_flask_response(
        error_response(ErrorCode.EMAIL_INVALID, 'Email invalid'))
    return create_flask_response(RestApiResponse(HTTPStatus.OK, {}))

  def get_registration_request(token: str) -> Response:
    registration = find_registration_token(token)
    if registration:
      return create_flask_response(RestApiResponse(HTTPStatus.OK, {
        'email': registration.email,
      }))
    return create_flask_response(RestApiResponse(HTTPStatus.NOT_FOUND, {}))

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
      registration_controller: AccountRegistrationController,
) -> list:
  def account_response_dict(account: Account):
    return {
      'username': account.username,
      'birderId': account.birder_id
    }

  def create_account() -> Response:
    token = request.json.get('token')
    username = request.json.get('username')
    password = request.json.get('password')
    registration = account_repository.find_account_registration_by_token(
      token)
    response = registration_controller.perform_registration(
      registration.email, registration.token, username, password)
    if response == 'success':
      account = account_repository.find_account(username)
      return create_flask_response(RestApiResponse(HTTPStatus.CREATED, {
        'id': account.id,
        'username': account.username,
        'email': account.email,
        'birder': {
          'id': account.birder.id,
          'name': account.birder.name,
        },
      }))
    elif response == 'username taken':
      return create_flask_response(error_response(
        ErrorCode.USERNAME_TAKEN,
        'Username taken',
        HTTPStatus.CONFLICT,
      ))

  @require_authentication(jwt_decoder, account_repository)
  def get_accounts(account: Account) -> Response:
    accounts = account_repository.accounts()
    response = RestApiResponse(HTTPStatus.OK, {
      'items': list(map(account_response_dict, accounts))
    })
    return create_flask_response(response)

  @require_authentication(jwt_decoder, account_repository)
  def get_me(account: Account) -> Response:
    response = RestApiResponse(HTTPStatus.OK, account_response_dict(account))
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
