import datetime
import logging
import os
from typing import Optional

from flask import Flask
from flask import request
from flask_cors import CORS

from .sqlalchemy_database import EngineFactory, SessionFactory
from .search_api import create_search_api_blueprint
from .birders_rest_api import create_birder_rest_api_blueprint
from .sighting_rest_api import create_sighting_rest_api_blueprint
from .account import AccountRepository, AccountFactory
from .account import PasswordHasher
from .account import PasswordRepository
from .account import TokenFactory
from .authentication import AccountRegistrationController
from .authentication import PasswordUpdateController
from .authentication import RefreshTokenRepository
from .authentication import JwtFactory
from .authentication import JwtDecoder
from .authentication import AuthenticationTokenFactory
from .authentication import Authenticator
from .authentication import PasswordResetController
from .authentication import SaltFactory
from .authentication_rest_api import create_authentication_rest_api_blueprint
from .birds_rest_api import BirdsRestApi
from .account_rest_api import create_account_rest_api_blueprint
from .bird import BirdRepository
from .link import LinkFactory
from .localization import LocaleRepository, LocaleDeterminerFactory
from .localization import LoadedLocale
from .localization import LocaleLoader, Locale
from .mail import MailDispatcherFactory
from .birder import BirderRepository
from .picture import PictureRepository
from .search import BirdSearchController
from .search import BirdSearcher
from .search import StringMatcher
from .settings_blueprint import update_locale_context
from .sighting import SightingRepository
from .v0 import create_api_v0_blueprint


def create_app(test_config: Optional[dict] = None) -> Flask:
  app = Flask(__name__, instance_relative_config=True)
  configure_app(app, test_config)

  # Create blueprint dependencies
  user_locale_cookie_key = 'user_locale'
  database_connection_details = create_database_connection_details()
  engine_factory = EngineFactory()
  engine = engine_factory.create_engine(**database_connection_details)
  session_factory = SessionFactory(engine)
  session = session_factory.create_session()
  salt_factory = SaltFactory()
  hasher = PasswordHasher(salt_factory)
  token_factory = TokenFactory()
  account_repository = AccountRepository(hasher, session)
  mail_dispatcher_factory = MailDispatcherFactory(app)
  mail_dispatcher = mail_dispatcher_factory.create_dispatcher()
  birder_repository = BirderRepository(session)
  authenticator = Authenticator(account_repository, hasher)
  localespath = os.path.join(app.root_path, 'locales')
  locales_misses_repository = {}
  locale_loader = LocaleLoader(localespath, locales_misses_repository)
  locale_repository = LocaleRepository(localespath, locale_loader, session)
  locale_determiner_factory = LocaleDeterminerFactory(user_locale_cookie_key,
                                                      locale_repository)
  bird_repository = BirdRepository(session)
  string_matcher = StringMatcher()
  bird_searcher = BirdSearcher(
    bird_repository, locale_repository, string_matcher, locale_loader)
  sighting_repository = SightingRepository(session)
  picture_repository = PictureRepository(session)
  link_factory = LinkFactory(
    os.environ['EXTERNAL_HOST'],
    app.config['FRONTEND_HOST'],
  )
  password_repository = PasswordRepository(token_factory, hasher, session)
  account_factory = AccountFactory(hasher, account_repository,
                                   password_repository)
  account_registration_controller = AccountRegistrationController(
    account_factory, account_repository, mail_dispatcher, link_factory,
    birder_repository, token_factory)
  bird_search_controller = BirdSearchController(bird_searcher)
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
  jwt_factory = JwtFactory(app.secret_key)
  authentication_token_factory = AuthenticationTokenFactory(
    jwt_factory, datetime.datetime.utcnow)
  jwt_decoder = JwtDecoder(app.secret_key)
  birds_rest_api = BirdsRestApi(
    link_factory,
    bird_repository,
    picture_repository
  )

  # Create and register blueprints
  authentication_blueprint = create_authentication_rest_api_blueprint(
    account_repository,
    authenticator,
    password_reset_controller,
    account_registration_controller,
    locale_repository,
    locale_loader,
    jwt_decoder,
    password_update_controller,
    refresh_token_repository,
    authentication_token_factory,
  )
  birder_rest_api = create_birder_rest_api_blueprint(
    jwt_decoder,
    account_repository,
    birder_repository,
    sighting_repository,
  )
  account_rest_api = create_account_rest_api_blueprint(
    jwt_decoder, account_repository)
  api_v0_blueprint = create_api_v0_blueprint(birds_rest_api)
  sighting_api = create_sighting_rest_api_blueprint(
    jwt_decoder,
    account_repository,
    sighting_repository,
    bird_repository,
  )
  search_api_blueprint = create_search_api_blueprint(
    bird_search_controller,
    bird_repository,
    picture_repository,
    link_factory
  )
  app.register_blueprint(api_v0_blueprint)
  app.register_blueprint(sighting_api)
  app.register_blueprint(authentication_blueprint)
  app.register_blueprint(account_rest_api)
  app.register_blueprint(birder_rest_api)
  app.register_blueprint(search_api_blueprint)

  @app.before_request
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

  app.logger.info('Flask app constructed')
  return app


def configure_app(app: Flask, test_config: dict) -> None:
  if not os.path.isdir(app.instance_path):
    os.makedirs(app.instance_path)
  if test_config:
    app.config.from_mapping(test_config)
  else:
    app.config.from_pyfile('config.py', silent=True)
  if not app.config['SECRET_KEY']:
    raise Exception('Flask secret key not set')
  if not os.path.isdir(app.config['LOGS_DIR_PATH']):
    os.makedirs(app.config['LOGS_DIR_PATH'])
  if 'FRONTEND_HOST' not in app.config and 'FRONTEND_HOST' in os.environ:
    app.config['FRONTEND_HOST'] = os.environ['FRONTEND_HOST']
  elif 'FRONTEND_HOST' not in app.config:
    raise Exception('FRONTEND_HOST not set in environment variables or config.')
  configure_cross_origin_resource_sharing(app)


def configure_cross_origin_resource_sharing(app: Flask) -> None:
  logging.getLogger('flask_cors').level = logging.DEBUG
  CORS(app, resources={
    r'/*': {
      'supports_credentials': True,
      'expose_headers': 'Location',
      'origins': app.config['FRONTEND_HOST']
    }
  })


def create_database_connection_details() -> dict:
  return {
    'host': os.environ.get('DATABASE_HOST'),
    'dbname': os.environ.get('DATABASE_NAME'),
    'user': os.environ.get('DATABASE_USER'),
    'password': os.environ.get('DATABASE_PASSWORD')
  }
