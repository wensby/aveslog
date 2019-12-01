import os
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from typing import Callable, Union, Optional, List

from flask import Response, request, make_response, jsonify, current_app, g

from aveslog.v0 import accounts_rest_api
from aveslog.v0.time import parse_date
from aveslog.v0.time import parse_time
from aveslog.v0.sighting import SightingRepository
from aveslog.v0.birds_rest_api import bird_summary_representation
from aveslog.v0.birds_rest_api import get_single_bird
from aveslog.v0.localization import LoadedLocale, LocaleRepository, LocaleLoader
from aveslog.v0.link import LinkFactory
from aveslog.v0.account import is_valid_password
from aveslog.v0.authentication import JwtDecoder, AccountRegistrationController, \
  Authenticator, AuthenticationTokenFactory, \
  PasswordResetController, PasswordUpdateController
from aveslog.v0.error import ErrorCode
from aveslog.v0.models import Account, Bird, Picture, AccountRegistration, \
  RefreshToken, Sighting, Birder
from aveslog.v0.rest_api import error_response
from aveslog.v0.search import BirdSearchMatch, StringMatcher
from aveslog.v0.search import BirdSearcher

RouteFunction = Callable[..., Response]


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


def create_birds_routes():
  routes = [
    {
      'rule': '/birds/<string:bird_identifier>',
      'func': get_single_bird,
    },
  ]

  return routes


def create_search_routes(
      link_factory: LinkFactory,
      string_matcher: StringMatcher,
):
  def _external_picture_url(picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return link_factory.create_url_external_link(static_picture_url)

  def _result_item(match: BirdSearchMatch, embed: list) -> dict:
    bird = match.bird
    item = bird_summary_representation(bird)
    item['score'] = match.score
    if 'thumbnail' in embed and bird.thumbnail:
      item['thumbnail'] = {
        'url': _external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit
      }
    return item

  def search_birds() -> Response:
    query = request.args.get('q')
    page_size = request.args.get('page_size', type=int)
    embed = parse_embed_list(request.args)
    page_size = page_size if page_size else 30
    embed = embed if embed else []
    bird_searcher = BirdSearcher(
      g.database_session,
      string_matcher,
    )
    search_matches = bird_searcher.search(query)
    search_matches.sort(key=lambda m: m.score, reverse=True)
    bird_matches = list(
      map(lambda x: _result_item(x, embed), search_matches[:page_size]))
    return make_response(jsonify({
      'items': bird_matches,
    }), HTTPStatus.OK)

  def parse_embed_list(args):
    return args.get('embed', type=str).split(',') if 'embed' in args else []

  return [
    {
      'rule': '/search/birds',
      'func': search_birds,
    }
  ]


def create_registration_routes(
      registration_controller: AccountRegistrationController,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
) -> list:
  def find_registration_token(registration_token: str) -> Optional[
    AccountRegistration]:
    return g.database_session.query(AccountRegistration). \
      filter(AccountRegistration.token.like(registration_token)).first()

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
      return error_response(ErrorCode.EMAIL_TAKEN, 'Email taken')
    elif result == 'email invalid':
      return error_response(ErrorCode.EMAIL_INVALID, 'Email invalid')
    return make_response('', HTTPStatus.OK)

  def get_registration_request(token: str) -> Response:
    registration = find_registration_token(token)
    if registration:
      return make_response(jsonify({
        'email': registration.email,
      }), HTTPStatus.OK)
    return make_response('', HTTPStatus.NOT_FOUND)

  return [
    {
      'rule': '/registration-requests',
      'func': post_registration_request,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/registration-requests/<string:token>',
      'func': get_registration_request,
    },
  ]


def create_account_routes() -> list:
  def account_response_dict(account: Account):
    return {
      'username': account.username,
      'birderId': account.birder_id
    }

  @require_authentication
  def get_accounts() -> Response:
    accounts = g.database_session.query(Account).all()
    return make_response(jsonify({
      'items': list(map(account_response_dict, accounts))
    }), HTTPStatus.OK)

  @require_authentication
  def get_account(username: str) -> Response:
    session = g.database_session
    account = session.query(Account).filter_by(username=username).first()
    if not account:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response(jsonify(account_response_dict(account)), HTTPStatus.OK)

  @require_authentication
  def get_me() -> Response:
    account = g.authenticated_account
    return make_response(jsonify(account_response_dict(account)), HTTPStatus.OK)

  return [
    {
      'rule': '/accounts/<string:username>',
      'func': get_account,
    },
    {
      'rule': '/accounts',
      'func': accounts_rest_api.create_account,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/accounts',
      'func': get_accounts,
    },
    {
      'rule': '/account',
      'func': get_me,
    },
  ]


def create_authentication_routes(
      jwt_decoder: JwtDecoder,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
      authenticator: Authenticator,
      token_factory: AuthenticationTokenFactory,
      password_reset_controller: PasswordResetController,
      password_update_controller: PasswordUpdateController,
) -> list:
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

  def create_persistent_refresh_token(account: Account) -> RefreshToken:
    session = g.database_session
    token = token_factory.create_refresh_token(account.id)
    session.add(token)
    session.commit()
    return token

  def post_refresh_token() -> Response:
    username = request.args.get('username')
    password = request.args.get('password')
    session = g.database_session
    account = session.query(Account).filter_by(username=username).first()
    if not account:
      return credentials_incorrect_response()
    if not authenticator.is_account_password_correct(account, password):
      return credentials_incorrect_response()
    refresh_token = create_persistent_refresh_token(account)
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
    access_token = token_factory.create_access_token(account_id)
    return make_response(jsonify({
      'jwt': access_token.jwt,
      'expiresIn': (access_token.expiration_date - datetime.now()).seconds,
    }), HTTPStatus.OK)

  def initiate_password_reset(email: str) -> bool:
    locale = load_english_locale()
    return password_reset_controller.initiate_password_reset(email, locale)

  def load_english_locale() -> LoadedLocale:
    locale = locale_repository.find_locale_by_code('en')
    return locale_loader.load_locale(locale)

  def post_password_reset_email() -> Response:
    email = request.json['email']
    created = initiate_password_reset(email)
    if not created:
      return error_response(
        ErrorCode.EMAIL_MISSING,
        'E-mail not associated with any account',
      )
    return make_response('', HTTPStatus.OK)

  def try_perform_password_reset(password: str,
        password_reset_token: str) -> str:
    return password_reset_controller.perform_password_reset(
      password_reset_token, password)

  def post_password_reset(token: str) -> Response:
    password = request.json['password']
    success = try_perform_password_reset(password, token)
    if not success:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response('', HTTPStatus.OK)

  def is_password_correct(account: Account, password: str) -> bool:
    return authenticator.is_account_password_correct(account, password)

  @require_authentication
  def post_password() -> Response:
    account = g.authenticated_account
    old_password = request.json['oldPassword']
    new_password = request.json['newPassword']
    old_password_correct = is_password_correct(account, old_password)
    if not old_password_correct:
      return error_response(
        ErrorCode.OLD_PASSWORD_INCORRECT,
        'Old password incorrect',
        status_code=HTTPStatus.UNAUTHORIZED,
      )
    if not is_valid_password(new_password):
      return error_response(ErrorCode.PASSWORD_INVALID, 'New password invalid')
    password_update_controller.update_password(account, new_password)
    return make_response('', HTTPStatus.NO_CONTENT)

  return [
    {
      'rule': '/authentication/refresh-token',
      'func': post_refresh_token,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/refresh-token/<int:refresh_token_id>',
      'func': delete_refresh_token,
      'options': {'methods': ['DELETE']},
    },
    {
      'rule': '/authentication/access-token',
      'func': get_access_token,
    },
    {
      'rule': '/authentication/password-reset',
      'func': post_password_reset_email,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/password-reset/<string:token>',
      'func': post_password_reset,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/password',
      'func': post_password,
      'options': {'methods': ['POST']},
    },
  ]


def create_sightings_routes(sighting_repository: SightingRepository) -> list:
  @require_authentication
  def get_birder_sightings(birder_id: int):
    (sightings, total_rows) = sighting_repository.sightings(
      birder_id=birder_id)
    return sightings_response(sightings, False)

  @require_authentication
  def get_sightings():
    limit = request.args.get('limit', type=int)
    if limit is not None and limit <= 0:
      return sightings_failure_response('limit-invalid')
    (sightings, total_rows) = sighting_repository.sightings(limit=limit)
    has_more = total_rows > limit if limit is not None else False
    return sightings_response(sightings, has_more)

  @require_authentication
  def get_sighting(sighting_id: int) -> Response:
    account = g.authenticated_account
    sighting = sighting_repository.find_sighting(sighting_id)
    if sighting and sighting.birder_id == account.birder_id:
      return make_response(jsonify(convert_sighting(sighting)), HTTPStatus.OK)
    else:
      return get_sighting_failure_response()

  @require_authentication
  def delete_sighting(sighting_id: int) -> Response:
    account = g.authenticated_account
    sighting = sighting_repository.find_sighting(sighting_id)
    if not sighting:
      return sighting_deleted_response()
    if sighting.birder_id != account.birder_id:
      return sighting_delete_unauthorized_response()
    sighting_repository.delete_sighting(sighting_id)
    return sighting_deleted_response()

  @require_authentication
  def post_sighting() -> Response:
    account = g.authenticated_account
    birder_id = request.json['birder']['id']
    if account.birder_id != birder_id:
      return post_sighting_unauthorized_response()
    binomial_name = request.json['bird']['binomialName']
    bird = g.database_session.query(Bird).filter(
      Bird.binomial_name.ilike(binomial_name)).first()
    if not bird:
      return make_response('', HTTPStatus.BAD_REQUEST)
    sighting = create_sighting(request.json, bird)
    sighting = sighting_repository.add_sighting(sighting)
    return post_sighting_success_response(sighting.id)

  return [
    {
      'rule': '/birders/<int:birder_id>/sightings',
      'func': get_birder_sightings,
    },
    {
      'rule': '/sightings',
      'func': get_sightings,
    },
    {
      'rule': '/sightings/<int:sighting_id>',
      'func': get_sighting,
    },
    {
      'rule': '/sightings/<int:sighting_id>',
      'func': delete_sighting,
      'options': {'methods': ['DELETE']},
    },
    {
      'rule': '/sightings',
      'func': post_sighting,
      'options': {'methods': ['POST']},
    },
  ]
  pass


def create_birders_routes() -> list:
  @require_authentication
  def get_birder(birder_id: int):
    birder = g.database_session.query(Birder).get(birder_id)
    if not birder:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response(jsonify(convert_birder(birder)), HTTPStatus.OK)

  return [
    {
      'rule': '/birders/<int:birder_id>',
      'func': get_birder,
    },
  ]


def convert_birder(birder: Birder) -> dict:
  return {
    'id': birder.id,
    'name': birder.name,
  }


def sightings_response(sightings: List[Sighting], has_more: bool) -> Response:
  return make_response(jsonify({
    'items': list(map(convert_sighting, sightings)),
    'hasMore': has_more,
  }), HTTPStatus.OK)


def sightings_failure_response(error_message):
  return make_response(jsonify({
    'error': error_message,
  }), HTTPStatus.BAD_REQUEST)


def convert_sighting(sighting: Sighting) -> dict:
  result = {
    'id': sighting.id,
    'birderId': sighting.birder_id,
    'birdId': sighting.bird.binomial_name.lower().replace(' ', '-'),
    'date': sighting.sighting_date.isoformat(),
  }
  if sighting.sighting_time:
    result['time'] = sighting.sighting_time.isoformat()
  return result


def get_sighting_failure_response() -> Response:
  return make_response(jsonify({
    'status': 'failure',
    'message': 'You are not authorized to get this sighting'
  }), HTTPStatus.UNAUTHORIZED)


def sighting_deleted_response() -> Response:
  return make_response('', HTTPStatus.NO_CONTENT)


def sighting_delete_unauthorized_response() -> Response:
  return make_response('', HTTPStatus.UNAUTHORIZED)


def create_sighting(post_data: dict, bird: Bird) -> Sighting:
  return Sighting(
    birder_id=post_data['birder']['id'], bird_id=bird.id,
    sighting_date=parse_date(post_data['date']),
    sighting_time=parse_time(
      post_data['time']) if 'time' in post_data else None)


def post_sighting_success_response(sighting_id: int) -> Response:
  response = make_response(jsonify({
    'status': 'success',
  }), HTTPStatus.CREATED)
  response.headers['Location'] = f'/sightings/{sighting_id}'
  response.autocorrect_location_header = False
  return response


def post_sighting_unauthorized_response() -> Response:
  return make_response(jsonify({
    'status': 'failure',
  }), HTTPStatus.UNAUTHORIZED)
