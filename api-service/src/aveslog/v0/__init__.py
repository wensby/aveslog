import datetime
from http import HTTPStatus

from flask import Blueprint, request, after_this_request, g

from aveslog.v0.database import EngineFactory
from aveslog.v0.database import SessionFactory
from aveslog.v0.sighting import SightingRepository
from aveslog.v0.birder import BirderRepository
from aveslog.v0.error import ErrorCode
from aveslog.v0.mail import MailDispatcher
from aveslog.v0.account import AccountRepository
from aveslog.v0.account import TokenFactory
from aveslog.v0.account import AccountFactory
from aveslog.v0.account import PasswordHasher
from aveslog.v0.account import PasswordRepository
from aveslog.v0.authentication import AccountRegistrationController
from aveslog.v0.authentication import JwtFactory
from aveslog.v0.authentication import PasswordResetController
from aveslog.v0.authentication import PasswordUpdateController
from aveslog.v0.authentication import SaltFactory
from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.authentication import RefreshTokenRepository
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.authentication import Authenticator
from aveslog.v0.localization import Locale
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.localization import LocaleDeterminerFactory
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.link import LinkFactory
from aveslog.v0.rest_api import error_response
from aveslog.v0.rest_api import create_flask_response
from aveslog.v0.bird import BirdRepository
from aveslog.v0.routes import create_birds_routes
from aveslog.v0.routes import create_sightings_routes
from aveslog.v0.routes import create_birders_routes
from aveslog.v0.routes import create_authentication_routes
from aveslog.v0.routes import create_registration_routes
from aveslog.v0.routes import create_account_routes
from aveslog.v0.routes import create_search_routes
from aveslog.v0.search import StringMatcher
from aveslog.v0.search import BirdSearcher


def create_api_v0_blueprint(
      mail_dispatcher: MailDispatcher,
      secret_key: str,
      api_external_host: str,
      frontend_host: str,
      localespath: str,
      user_locale_cookie_key: str,
      database_connection_details,
) -> Blueprint:
  def register_routes(routes):
    for route in routes:
      rule = route['rule']
      endpoint = route.get('endpoint', None)
      view_func = route['func']
      options = route.get('options', {})
      blueprint.add_url_rule(rule, endpoint, view_func, **options)
      blueprint.add_url_rule(f'/v0{rule}', endpoint, view_func, **options)

  engine_factory = EngineFactory()
  engine = engine_factory.create_engine(**database_connection_details)
  session_factory = SessionFactory(engine)
  session = session_factory.create_session()
  locales_misses_repository = {}
  locale_loader = LocaleLoader(localespath, locales_misses_repository)
  locale_repository = LocaleRepository(localespath, locale_loader, session)
  locale_determiner_factory = LocaleDeterminerFactory(user_locale_cookie_key,
    locale_repository)
  salt_factory = SaltFactory()
  password_hasher = PasswordHasher(salt_factory)
  jwt_decoder = JwtDecoder(secret_key)
  link_factory = LinkFactory(api_external_host, frontend_host)
  bird_repository = BirdRepository(session)
  token_factory = TokenFactory()
  password_repository = PasswordRepository(token_factory, password_hasher,
    session)
  account_repository = AccountRepository(password_hasher, session)
  account_factory = AccountFactory(
    password_hasher,
    account_repository,
    password_repository,
  )
  birder_repository = BirderRepository(session)
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
  sighting_repository = SightingRepository(session)

  blueprint = Blueprint('v0', __name__)
  birds_routes = create_birds_routes(bird_repository, link_factory)
  register_routes(birds_routes)
  search_routes = create_search_routes(bird_searcher, link_factory)
  register_routes(search_routes)
  registration_routes = create_registration_routes(
    account_registration_controller,
    account_repository,
    locale_repository,
    locale_loader,
  )
  register_routes(registration_routes)
  sighting_routes = create_sightings_routes(
    jwt_decoder,
    account_repository,
    sighting_repository,
    bird_repository,
  )
  register_routes(sighting_routes)
  authentication_routes = create_authentication_routes(
    jwt_decoder,
    account_repository,
    locale_repository,
    locale_loader,
    authenticator,
    authentication_token_factory,
    refresh_token_repository,
    password_reset_controller,
    password_update_controller,
  )
  register_routes(authentication_routes)
  account_routes = create_account_routes(
    jwt_decoder,
    account_repository,
    account_registration_controller)
  register_routes(account_routes)
  birders_routers = create_birders_routes(
    jwt_decoder,
    account_repository,
    birder_repository,
    sighting_repository,
  )
  register_routes(birders_routers)

  @blueprint.before_request
  def before_request():
    detect_user_locale()

  def detect_user_locale():
    locale_determiner = locale_determiner_factory.create_locale_determiner()
    locale_code = locale_determiner.determine_locale_from_request(request)
    if locale_code:
      locale = locale_repository.find_locale_by_code(locale_code)
      loaded_locale = locale_loader.load_locale(locale)
      update_locale_context(user_locale_cookie_key, loaded_locale)
    else:
      update_locale_context(
        user_locale_cookie_key,
        LoadedLocale(Locale(id=None, code=None), None, None, None))

  @blueprint.app_errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
  def too_many_requests_handler(e):
    return create_flask_response(error_response(
      ErrorCode.RATE_LIMIT_EXCEEDED,
      f'Rate limit exceeded {e.description}',
      HTTPStatus.TOO_MANY_REQUESTS,
    ))

  return blueprint


def update_locale_context(user_locale_cookie_key, loaded_locale: LoadedLocale):
  previously_set_code = request.cookies.get(user_locale_cookie_key, None)
  # when the response exists, set a cookie with the language if it is new
  if loaded_locale.locale.code and loaded_locale.locale.code is not previously_set_code:
    set_locale_cookie_after_this_request(loaded_locale.locale,
      user_locale_cookie_key)
  g.locale = loaded_locale


def set_locale_cookie_after_this_request(locale: Locale,
      user_locale_cookie_key):
  @after_this_request
  def set_locale_cookie(response):
    response.set_cookie(user_locale_cookie_key, locale.code)
    return response
