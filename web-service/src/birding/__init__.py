import os
from flask import Flask, g, request, after_this_request, redirect, url_for
from .database import DatabaseConnector
from .user_account import UserAccountRepository
from .user_account import PasswordHasher
from .user_account import Credentials
from .user_account import Authenticator
from .mail import MailDispatcherFactory
from .person import PersonRepository
from .authentication import create_authentication_blueprint
from .blueprint_search import create_search_blueprint
from .blueprint_sighting import create_sighting_blueprint
from .blueprint_profile import create_profile_blueprint
from .localization import LocaleDeterminer
from .localization import LocalesFactory
from .bird import BirdRepository
from .search import BirdSearcher
from .sighting import SightingRepository

def create_app(test_config=None):
  secret_key = open('secret_key', 'r').readline()
  app = Flask(__name__, instance_relative_config=True)
  app.config['SECRET_KEY'] = secret_key
  
  if test_config:
    app.config.from_mapping(test_config)
  else:
    app.config.from_pyfile('config.py', silent=True)

  if not os.path.isdir(app.instance_path):
    os.makedirs(app.instance_path)

  # Create blueprint dependencies
  user_locale_cookie_key = 'user_locale'
  database = DatabaseConnector.connect('birding-database-service', 'birding-database', 'postgres', 'docker')
  hasher = PasswordHasher()
  account_repository = UserAccountRepository(database, hasher)
  mail_dispatcher_factory = MailDispatcherFactory(app)
  mail_dispatcher = mail_dispatcher_factory.create_dispatcher()
  person_repository = PersonRepository(database)
  authenticator = Authenticator(account_repository, hasher)
  localespath = os.path.join(app.root_path, 'locales/')
  locales_factory = LocalesFactory(database, localespath)
  locales = locales_factory.create_locales()
  locale_determiner = LocaleDeterminer(locales, user_locale_cookie_key)
  bird_repository = BirdRepository(database)
  bird_searcher = BirdSearcher(bird_repository, locales)
  sighting_repository = SightingRepository(database)

  # Create and register blueprints
  authentication_blueprint = create_authentication_blueprint(
      account_repository, mail_dispatcher, person_repository, authenticator
  )
  search_blueprint = create_search_blueprint(bird_searcher, account_repository)
  sighting_blueprint = create_sighting_blueprint(account_repository, sighting_repository, bird_repository)
  profile_blueprint = create_profile_blueprint(account_repository)
  app.register_blueprint(authentication_blueprint)
  app.register_blueprint(search_blueprint)
  app.register_blueprint(sighting_blueprint)
  app.register_blueprint(profile_blueprint)

  @app.before_request
  def before_request():
    # initialize render context dictionary
    g.render_context = dict()
    detect_user_locale()
  
  def detect_user_locale():
    locale = locale_determiner.determine_locale_from_request(request)
    update_locale_context(locale)
  
  def update_locale_context(locale):
    previously_set = request.cookies.get(user_locale_cookie_key, None)
    # when the response exists, set a cookie with the language if it is new
    if not previously_set or previously_set is not locale.language.iso_639_1_code:
      set_locale_cookie_after_this_request(locale)
    g.render_context['locale'] = locale
  
  def set_locale_cookie_after_this_request(locale):
    @after_this_request
    def remember_language(response):
      response.set_cookie(user_locale_cookie_key, locale.language.iso_639_1_code)
      return response

  @app.route('/language')
  def language():
    language_code = request.args.get('l')
    languages = list(filter(lambda l: l.iso_639_1_code == language_code, locales))
    if languages:
      language = languages[0]
      locale = locales[language]
      update_locale_context(locale)
      return redirect(url_for('sighting.index'))

  return app
