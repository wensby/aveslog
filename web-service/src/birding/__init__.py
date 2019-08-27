import datetime
import logging
import os

from flask import Flask, session
from flask import g
from flask import request
from flask_cors import CORS

from .account import AccountRepository, AccountFactory
from .account import PasswordHasher
from .account import PasswordRepository
from .account import TokenFactory
from .authentication import AccountRegistrationController
from .authentication import AuthenticationTokenDecoder
from .authentication import AuthenticationTokenFactory
from .authentication import Authenticator
from .authentication import PasswordResetController
from .authentication import SaltFactory
from .authentication_blueprint import create_authentication_blueprint
from .authentication_reset_api import create_authentication_rest_api_blueprint
from .rest_bird import create_v2_bird_blueprint
from .account_rest_api import create_account_rest_api_blueprint
from .bird import BirdRepository
from .bird_view import BirdViewFactory
from .bird_blueprint import create_bird_blueprint
from .blueprint_home import create_home_blueprint
from .profile_blueprint import create_profile_blueprint
from .database import DatabaseFactory
from .link import LinkFactory
from .localization import LocaleRepository, LocaleDeterminerFactory, \
  LocalesMissesLogger
from .localization import LoadedLocale
from .localization import LocaleLoader, Locale
from .mail import MailDispatcherFactory
from .person import PersonRepository
from .picture import PictureRepository
from .search import BirdSearchController
from .search import BirdSearcher
from .search import StringMatcher
from .search_view import BirdSearchViewFactory
from .settings_blueprint import create_settings_blueprint, update_locale_context
from .sighting import SightingRepository
from .sighting_blueprint import create_sighting_blueprint
from .sighting_view import SightingViewFactory


def create_app(test_config=None):
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
  localespath = os.path.join(app.root_path, 'locales/')
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
  bird_search_view_factory = BirdSearchViewFactory(picture_repository,
                                                   bird_repository)
  sighting_view_factory = SightingViewFactory(bird_repository, database)
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
  password_reset_controller = PasswordResetController(
    account_repository, password_repository, link_factory, mail_dispatcher)
  locales_misses_logger = LocalesMissesLogger(
    locales_misses_repository, app.config['LOGS_DIR_PATH'])
  authentication_token_factory = AuthenticationTokenFactory(
    app.secret_key, datetime.datetime.utcnow)
  authentication_token_decoder = AuthenticationTokenDecoder(app.secret_key)

  # Create and register blueprints
  home_blueprint = create_home_blueprint()
  authentication_blueprint = create_authentication_blueprint(
    account_repository,
    authenticator,
    account_registration_controller,
    password_reset_controller,
  )
  v2_authentication_blueprint = create_authentication_rest_api_blueprint(
    authenticator,
    password_reset_controller,
    account_registration_controller,
    locale_repository,
    locale_loader,
    authentication_token_factory,
  )
  account_rest_api = create_account_rest_api_blueprint(
    authentication_token_decoder, account_repository)
  sighting_blueprint = create_sighting_blueprint(sighting_repository,
                                                 sighting_view_factory)
  profile_blueprint = create_profile_blueprint(
    account_repository, sighting_repository)
  settings_blueprint = create_settings_blueprint(authenticator,
                                                 password_repository,
                                                 locale_repository,
                                                 account_repository,
                                                 locale_loader,
                                                 user_locale_cookie_key)
  bird_blueprint = create_bird_blueprint(bird_view_factory,
                                         bird_search_controller,
                                         bird_search_view_factory)
  v2_bird_blueprint = create_v2_bird_blueprint(
    bird_search_controller, bird_repository, picture_repository, link_factory)
  app.register_blueprint(v2_bird_blueprint)
  app.register_blueprint(home_blueprint)
  app.register_blueprint(authentication_blueprint)
  app.register_blueprint(sighting_blueprint)
  app.register_blueprint(profile_blueprint)
  app.register_blueprint(settings_blueprint)
  app.register_blueprint(bird_blueprint)
  app.register_blueprint(v2_authentication_blueprint)
  app.register_blueprint(account_rest_api)

  @app.before_request
  def before_request():
    load_logged_in_account()
    init_render_context()
    detect_user_locale()

  @app.after_request
  def after_request(response):
    locales_misses_logger.log_misses()
    return response

  def load_logged_in_account():
    account_id = session.get('account_id')
    if account_id:
      g.logged_in_account = account_repository.find_account_by_id(account_id)
    else:
      g.logged_in_account = None

  def init_render_context():
    g.render_context = dict()

  def detect_user_locale():
    if g.logged_in_account:
      if g.logged_in_account.locale_id:
        locale = locale_repository.find_locale_by_id(
          g.logged_in_account.locale_id)
        loaded_locale = locale_loader.load_locale(locale)
        update_locale_context(user_locale_cookie_key, loaded_locale)
      else:
        update_locale_context(
          user_locale_cookie_key,
          LoadedLocale(Locale(None, None), None, None, None))
    else:
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


def configure_app(app, test_config):
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
  configure_cross_origin_resource_sharing(app)


def configure_cross_origin_resource_sharing(app: Flask):
  if 'FRONTEND_HOST' in app.config:
    frontend_host = app.config['FRONTEND_HOST']
  elif 'FRONTEND_HOST' in os.environ:
    frontend_host = os.environ['FRONTEND_HOST']
    app.config['FRONTEND_HOST'] = frontend_host
  else:
    raise Exception('FRONTEND_HOST not set in environment variables or config.')
  logging.getLogger('flask_cors').level = logging.DEBUG
  CORS(app, resources={
    r'/v2/*': {
      'supports_credentials': True,
      'origins': frontend_host
    }
  })


def create_database_connection_details():
  return {
    'host': os.environ.get('DATABASE_HOST'),
    'dbname': os.environ.get('DATABASE_NAME'),
    'user': os.environ.get('DATABASE_USER'),
    'password': os.environ.get('DATABASE_PASSWORD')
  }
