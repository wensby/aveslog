import datetime
from http import HTTPStatus

from flask import Blueprint
from sqlalchemy.orm import Session

from aveslog.v0.account_rest_api import AccountsRestApi
from aveslog.v0.birder import BirderRepository
from aveslog.v0.error import ErrorCode
from aveslog.v0.mail import MailDispatcher
from aveslog.v0.account import AccountRepository
from aveslog.v0.account import TokenFactory
from aveslog.v0.account import AccountFactory
from aveslog.v0.account import PasswordHasher
from aveslog.v0.account import PasswordRepository
from aveslog.v0.authentication import AccountRegistrationController, JwtFactory, \
  PasswordResetController, PasswordUpdateController
from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.authentication import RefreshTokenRepository
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.authentication import Authenticator
from aveslog.v0.authentication_rest_api import AuthenticationRestApi
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.link import LinkFactory
from aveslog.v0.registration_rest_api import RegistrationRestApi
from aveslog.v0.rest_api import error_response
from aveslog.v0.search_api import SearchApi
from aveslog.v0.bird import BirdRepository
from aveslog.v0.birds_rest_api import BirdsRestApi, create_flask_response
from aveslog.v0.routes import create_birds_routes
from aveslog.v0.routes import create_authentication_routes
from aveslog.v0.routes import create_registration_routes
from aveslog.v0.routes import create_account_routes
from aveslog.v0.routes import create_search_routes
from aveslog.v0.search import StringMatcher
from aveslog.v0.search import BirdSearcher


def create_api_v0_blueprint(
      link_factory: LinkFactory,
      bird_repository: BirdRepository,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
      account_repository: AccountRepository,
      password_hasher: PasswordHasher,
      mail_dispatcher: MailDispatcher,
      birder_repository: BirderRepository,
      jwt_decoder: JwtDecoder,
      secret_key: str,
      session: Session,
) -> Blueprint:
  def register_routes(routes):
    for route in routes:
      rule = route['rule']
      endpoint = route.get('endpoint', None)
      view_func = route['view_func']
      options = route.get('options', {})
      blueprint.add_url_rule(rule, endpoint, view_func, **options)
      blueprint.add_url_rule(f'/v0{rule}', endpoint, view_func, **options)

  token_factory = TokenFactory()
  password_repository = PasswordRepository(token_factory, password_hasher,
    session)
  account_factory = AccountFactory(
    password_hasher,
    account_repository,
    password_repository,
  )
  account_registration_controller = AccountRegistrationController(
    account_factory,
    account_repository,
    mail_dispatcher,
    link_factory,
    birder_repository,
    token_factory,
  )
  refresh_token_repository = RefreshTokenRepository(session)
  password_update_controller = PasswordUpdateController(
    password_repository,
    refresh_token_repository,
  )
  password_reset_controller = PasswordResetController(
    account_repository,
    password_repository,
    link_factory,
    mail_dispatcher,
    password_update_controller,
    token_factory,
  )
  birds_rest_api = BirdsRestApi(link_factory, bird_repository)
  string_matcher = StringMatcher()
  bird_searcher = BirdSearcher(
    bird_repository,
    locale_repository,
    string_matcher,
    locale_loader,
  )
  jwt_factory = JwtFactory(secret_key)
  authentication_token_factory = AuthenticationTokenFactory(
    jwt_factory,
    datetime.datetime.utcnow,
  )
  authenticator = Authenticator(account_repository, password_hasher)
  search_api = SearchApi(bird_searcher, bird_repository, link_factory)
  authentication_rest_api = AuthenticationRestApi(
    locale_repository,
    locale_loader,
    account_registration_controller,
    account_repository,
    authenticator,
    authentication_token_factory,
    refresh_token_repository,
    jwt_decoder,
    password_reset_controller,
    password_update_controller,
  )
  registration_rest_api = RegistrationRestApi(
    account_registration_controller,
    account_repository,
    locale_repository,
    locale_loader,
  )
  accounts_rest_api = AccountsRestApi(account_repository)

  blueprint = Blueprint('v0', __name__)
  birds_routes = create_birds_routes(birds_rest_api)
  register_routes(birds_routes)
  search_routes = create_search_routes(search_api)
  register_routes(search_routes)
  registration_routes = create_registration_routes(registration_rest_api)
  register_routes(registration_routes)
  authentication_routes = create_authentication_routes(
    authentication_rest_api,
    jwt_decoder,
    account_repository,
  )
  register_routes(authentication_routes)
  account_routes = create_account_routes(
    jwt_decoder,
    account_repository,
    accounts_rest_api)
  register_routes(account_routes)

  @blueprint.app_errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
  def too_many_requests_handler(e):
    return create_flask_response(error_response(
      ErrorCode.RATE_LIMIT_EXCEEDED,
      f'Rate limit exceeded {e.description}',
      HTTPStatus.TOO_MANY_REQUESTS,
    ))

  return blueprint
