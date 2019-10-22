import datetime
import logging
import os

from flask import Flask
from flask import request
from flask_cors import CORS

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
from .bird_rest_api import create_bird_rest_api_blueprint
from .account_rest_api import create_account_rest_api_blueprint
from .bird import BirdRepository
from .bird_view import BirdViewFactory
from .database import DatabaseFactory
from .link import LinkFactory
from .localization import LocaleRepository, LocaleDeterminerFactory
from .localization import LoadedLocale
from .localization import LocaleLoader, Locale
from .mail import MailDispatcherFactory
from .person import PersonRepository
from .picture import PictureRepository
from .search import BirdSearchController
from .search import BirdSearcher
from .search import StringMatcher
from .settings_blueprint import update_locale_context
from .sighting import SightingRepository


def create_app(test_config: dict = None) -> Flask:
  app = Flask(__name__, instance_relative_config=True)
  configure_app(app, test_config)

  # Create blueprint dependencies
  user_locale_cookie_key = 'user_locale'
  database_connection_factory = DatabaseFactory(app.logger)
  database_connection_details = create_database_connection_details()
  database = database_connection_factory.create_database(
    **database_connection_details)
  app.db = database
  salt_factory = SaltFactory()
  hasher = PasswordHasher(salt_factory)
  token_factory = TokenFactory()
  account_repository = AccountRepository(database, hasher, token_factory)
  mail_dispatcher_factory = MailDispatcherFactory(app)
  mail_dispatcher = mail_dispatcher_factory.create_dispatcher()
  person_repository = PersonRepository(database)
  authenticator = Authenticator(account_repository, hasher)
  localespath = os.path.join(app.root_path, 'locales')
  locales_misses_repository = {}
  locale_loader = LocaleLoader(localespath, locales_misses_repository)
  locale_repository = LocaleRepository(localespath, locale_loader, database)
  locale_determiner_factory = LocaleDeterminerFactory(user_locale_cookie_key,
                                                      locale_repository)
  bird_repository = BirdRepository(database)
  string_matcher = StringMatcher()
  bird_searcher = BirdSearcher(
    bird_repository, locale_repository, string_matcher, locale_loader)
  sighting_repository = SightingRepository(database)
  picture_repository = PictureRepository(database)
  link_factory = LinkFactory(
    os.environ['EXTERNAL_HOST'],
    app.config['FRONTEND_HOST'],
  )
  account_factory = AccountFactory(database, hasher)
  account_registration_controller = AccountRegistrationController(
    account_factory, account_repository, mail_dispatcher, link_factory,
    person_repository)
  bird_view_factory = BirdViewFactory(bird_repository, picture_repository)
  bird_search_controller = BirdSearchController(bird_searcher)
  password_repository = PasswordRepository(token_factory, database, hasher)
  refresh_token_repository = RefreshTokenRepository(database)
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
  )
  jwt_factory = JwtFactory(app.secret_key)
  authentication_token_factory = AuthenticationTokenFactory(
    jwt_factory, datetime.datetime.utcnow)
  jwt_decoder = JwtDecoder(app.secret_key)

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
  account_rest_api = create_account_rest_api_blueprint(
    jwt_decoder, account_repository)
  bird_rest_api = create_bird_rest_api_blueprint(
    bird_search_controller,
    bird_repository,
    picture_repository,
    link_factory,
    bird_view_factory
  )
  sighting_api = create_sighting_rest_api_blueprint(
    jwt_decoder,
    account_repository,
    sighting_repository,
    bird_repository,
  )
  app.register_blueprint(sighting_api)
  app.register_blueprint(bird_rest_api)
  app.register_blueprint(authentication_blueprint)
  app.register_blueprint(account_rest_api)

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
        LoadedLocale(Locale(None, None), None, None, None))

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
