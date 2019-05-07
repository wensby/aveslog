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
import birding_locale

app = Flask(__name__)

app.secret_key = open('/app/secret_key', 'r').readline()

hasher = PasswordHasher()
database = Database('birding-database-service', 'birding-database', 'postgres', 'docker')
bird_repo = BirdRepository(database)
sighting_repo = SightingRepository(database)
person_repo = PersonRepository(database)
account_repo = UserAccountRepository(database, hasher)
authenticator = Authenticator(account_repo, hasher)

@app.before_request
def before_request():
  # initialize render context dictionary
  g.render_context = dict()
  detect_user_language()

def detect_user_language():
  language = birding_locale.figure_out_language_from_request(request)
  update_language_context(language)

def update_language_context(language):
  if language not in birding_locale.language_dictionaries:
    return
  previously_set = request.cookies.get('user_lang', None)
  # when the response exists, set a cookie with the language if it is new
  if not previously_set or previously_set is not language:
    @after_this_request
    def remember_language(response):
      response.set_cookie('user_lang', language)
      return response
  g.language = language
  g.render_context['language_dic'] = birding_locale.language_dictionaries[language]

@app.route('/language', methods=['GET'])
def language():
  language = request.args.get('l')
  update_language_context(language)
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    account = account_repo.put_new_user_account(username, password)
    if account:
      flash('user account created')
      person = person_repo.add_person(username)
      account_repo.set_user_account_person(account, person)
      return redirect(url_for('get_login'))
    else:
      flash('user account not created')
      return redirect(url_for('register'))
  else:
    return render_page('register.html')

@app.route('/bird/search', methods=['GET'])
def bird_search():
  query = request.args.get('query')
  if re.compile('^[A-zåäöÅÄÖ ]+$').match(query):
    g.render_context['result'] = [query]
    if 'username' in session:
      g.render_context['username'] = session['username']
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
      session['username'] = account.username
      return redirect(url_for('index'))
  else:
    return redirect(url_for('get_login'))

@app.route('/login', methods=['GET'])
def get_login():
  return render_page('login.html')

@app.route('/logout', methods=['GET'])
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

def putbird(bird_name, sighting_time):
  if session['username']:
    person_name = session['username']
    person_id = person_repo.get_person_by_name(person_name).id
    bird = bird_repo.get_bird_by_name(bird_name)
    if not bird:
      bird = bird_repo.add_bird(bird_name)
    bird_id = bird.id
    sighting_repo.add_sighting(person_id, bird_id, sighting_time)

def getbirds():
  if session['username']:
    person_name = session['username']
    person_id = person_repo.get_person_by_name(person_name).id
    sightings = sighting_repo.get_sightings_by_person_id(person_id)
    birds = []
    for sighting in sightings:
      bird = bird_repo.get_bird_by_id(sighting.bird_id)
      if bird:
        birds.append((bird.name, sighting.sighting_time.isoformat(' ')))
    return birds

def render_page(page):
  return render_template(page, **g.render_context)

@app.route('/', methods=['GET', 'POST'])
def index():
  if 'username' in session:
    if request.method == 'POST':
      bird = request.form['bird']
      timezoneoffset = int(request.form['timezoneoffset'])
      sighting_time = datetime.utcnow() + timedelta(minutes=timezoneoffset)
      putbird(bird, sighting_time)
      return redirect(url_for('index'))
    else:
      birds = getbirds()
      g.render_context['username'] = session['username']
      g.render_context['birds'] = birds
      return render_page('index.html')
  else:
    return render_page('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3002, debug=True)
