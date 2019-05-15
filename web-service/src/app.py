import os.path
import re
import psycopg2
from pathlib import Path
from flask import Flask, request, redirect, url_for, session, render_template, flash, g, after_this_request
from sighting import SightingRepository
from bird import BirdRepository
from person import PersonRepository
from database import Database
from user_account import UserAccountRepository, PasswordHasher, Credentials, Authenticator
from datetime import datetime
from datetime import timedelta
from localization import LocaleDeterminer, LocalesFactory
from search import BirdSearcher

app = Flask(__name__)

app.secret_key = open('/app/secret_key', 'r').readline()

user_locale_cookie_key = 'user_locale'
hasher = PasswordHasher()
database = Database('birding-database-service', 'birding-database', 'postgres', 'docker')
bird_repo = BirdRepository(database)
sighting_repo = SightingRepository(database)
person_repo = PersonRepository(database)
account_repo = UserAccountRepository(database, hasher)
authenticator = Authenticator(account_repo, hasher)
locales_factory = LocalesFactory('locales/')
locales = locales_factory.create_locales(['en', 'sv', 'ko'])
locale_determiner = LocaleDeterminer(locales, user_locale_cookie_key)
bird_searcher = BirdSearcher(bird_repo, locales)

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

@app.route('/language', methods=['GET'])
def language():
  language_code = request.args.get('l')
  languages = list(filter(lambda l: l.iso_639_1_code == language_code, locales))
  if languages:
    language = languages[0]
    locale = locales[language]
    update_locale_context(locale)
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def post_register():
  username = request.form['username']
  password = request.form['password']
  account = account_repo.put_new_user_account(username, password)
  if account:
    flash('user account created')
    person = person_repo.add_person(username)
    account_repo.set_user_account_person(account, person)
    return redirect(url_for('get_register'))
  else:
    flash('user account not created')
    return redirect(url_for('get_register'))

@app.route('/sighting', methods=['POST'])
def post_sighting():
  bird_id = int(request.form['bird_id'])
  timezoneoffset = int(request.form['timezoneoffset'])
  sighting_time = datetime.utcnow() + timedelta(minutes=timezoneoffset)
  putbird(bird_id, sighting_time)
  return 'success?'

@app.route('/register', methods=['GET'])
def get_register():
  return render_page('register.html')

@app.route('/bird/search', methods=['GET'])
def bird_search():
  name = request.args.get('query')
  birds = bird_searcher.search(name)
  if re.compile('^[A-zåäöÅÄÖ ]+$').match(name):
    g.render_context['birds'] = list(birds)
    if 'account_id' in session:
      g.render_context['username'] = get_account(session['account_id']).username
    return render_page('birdsearch.html')
  else:
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def post_login():
  posted_username = request.form['username']
  posted_password = request.form['password']
  if Credentials.is_valid(posted_username, posted_password):
    credentials = Credentials(posted_username, posted_password)
    account = authenticator.get_authenticated_user_account(credentials)
    if account:
      session['account_id'] = account.id
      return redirect(url_for('index'))
  return redirect(url_for('get_login'))

@app.route('/login', methods=['GET'])
def get_login():
  return render_page('login.html')

@app.route('/logout', methods=['GET'])
def logout():
  session.pop('account_id', None)
  return redirect(url_for('index'))

def putbird(bird_id, sighting_time):
  if 'account_id' in session:
    person_id = get_account(session['account_id']).person_id
    sighting_repo.add_sighting(person_id, bird_id, sighting_time)

def get_sightings():
  if 'account_id' in session:
    person_id = get_account(session['account_id']).person_id
    sightings = sighting_repo.get_sightings_by_person_id(person_id)
    birds = []
    for sighting in sightings:
      bird = bird_repo.get_bird_by_id(sighting.bird_id)
      if bird:
        sighting_time = sighting.sighting_date.isoformat()
        if sighting.sighting_time:
          sighting_time = sighting_time + ' ' + sighting.sighting_time.isoformat()
        birds.append((bird.binomial_name, sighting_time))
    return birds

def render_page(page):
  return render_template(page, **g.render_context)

@app.route('/', methods=['GET'])
def index():
  if 'account_id' in session:
    birds = get_sightings()
    g.render_context['username'] = get_account(session['account_id']).username
    g.render_context['birds'] = birds
    #g.render_context['bird_dictionary'] = g.render_context['locale'].bird_dictionary
    return render_page('index.html')
  else:
    return render_page('index.html')

def get_account(id):
  return account_repo.get_user_account_by_id(id)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3002, debug=True)
