import os
from flask import Flask
from flask import g
from flask import request
from flask import after_this_request
from flask import redirect
from flask import url_for
from .database import DatabaseConnectionFactory
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
from .blueprint_settings import create_settings_blueprint
from .localization import LocaleDeterminer
from .localization import LocalesFactory
from .bird import BirdRepository
from .search import BirdSearcher
from .sighting import SightingRepository
from .render import render_page

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  configure_app(app, test_config)

  # Create blueprint dependencies
  user_locale_cookie_key = 'user_locale'
  database_connection_factory = DatabaseConnectionFactory(app.logger)
  database_connection_details = create_database_connection_details()
  database = database_connection_factory.create_connection(**database_connection_details)
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
  sighting_blueprint = create_sighting_blueprint(sighting_repository)
  profile_blueprint = create_profile_blueprint(account_repository)
  settings_blueprint = create_settings_blueprint(account_repository, authenticator)
  app.register_blueprint(authentication_blueprint)
  app.register_blueprint(search_blueprint)
  app.register_blueprint(sighting_blueprint)
  app.register_blueprint(profile_blueprint)
  app.register_blueprint(settings_blueprint)

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
      return redirect(url_for('index'))

  @app.route('/')
  def index():
    if g.logged_in_account:
      sightings = get_sightings()
      g.render_context['username'] = g.logged_in_account.username
      g.render_context['sightings'] = sightings
      return render_page('index.html')
    else:
      return render_page('index.html')

  def get_sightings():
    if g.logged_in_account:
      person_id = g.logged_in_account.person_id
      sightings = sighting_repository.get_sightings_by_person_id(person_id)
      result = []
      for sighting in sightings:
        bird = bird_repository.get_bird_by_id(sighting.bird_id)
        if bird:
          s = dict()
          sighting_time = sighting.sighting_date.isoformat()
          if sighting.sighting_time:
            sighting_time = sighting_time + ' ' + sighting.sighting_time.isoformat()
          s['bird'] = bird
          s['time'] = sighting_time
          thumbnail_image = find_thumbnail_image(bird)
          if thumbnail_image:
            s['thumbnail'] = thumbnail_image
          result.append(s)
      result.sort(reverse=True, key=lambda r: r['time'])
      return result

  def find_thumbnail_image(bird):
    birdname = bird.binomial_name.lower().replace(' ', '-')
    path = "image/bird/" + birdname + "-thumb.jpg"
    if os.path.isfile(app.root_path + "/static/" + path):
      return path

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

def create_database_connection_details():
  return {
      'host': os.environ.get('DATABASE_HOST'),
      'dbname': os.environ.get('DATABASE_NAME'),
      'user': os.environ.get('DATABASE_USER'),
      'password': os.environ.get('DATABASE_PASSWORD')
  }
