import os.path
import re
import psycopg2
from pathlib import Path
from flask import Flask, request, redirect, url_for, session, render_template, flash
from sighting import SightingRepository
from bird import BirdRepository
from person import PersonRepository
from database import Database
from user_account import UserAccountRepository, PasswordHasher, Credentials, Authenticator
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)

app.secret_key = open('/app/secret_key', 'r').readline()

hasher = PasswordHasher()
database = Database('birding-database-service', 'birding-database', 'postgres', 'docker')
bird_repo = BirdRepository(database)
sighting_repo = SightingRepository(database)
person_repo = PersonRepository(database)
account_repo = UserAccountRepository(database, hasher)
authenticator = Authenticator(account_repo, hasher)

def valid(text):
  return re.compile('^[A-z]{1,20}$').match(text)

def login_username():
  username = request.form['username']
  password = request.form['password']
  if valid(username) and valid(password):
    cred = Credentials(username, password)
    return authenticator.get_authenticated_user_account(cred)

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
      return redirect(url_for('login'))
    else:
      flash('user account not created')
      return redirect(url_for('register'))
  else:
    return render_template('register.html')

@app.route('/bird/search', methods=['GET'])
def bird_search():
  query = request.args.get('query')
  if re.compile('^[A-zåäöÅÄÖ ]+$').match(query):
    kwargs = dict()
    kwargs['result'] = [query]
    if 'username' in session:
      kwargs['username'] = session['username']
    return render_template('birdsearch.html', **kwargs)
  else:
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  app.logger.info('login %s', request.method)
  if request.method == 'POST':
    account = login_username()
    app.logger.info('%s logged in', account)
    if account:
      session['username'] = account.username
      return redirect(url_for('index'))
    else:
      return redirect(url_for('login'))
  else:
    return render_template('login.html')

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
        birds.append((bird.name, sighting.sighting_time))
    return birds

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
      return render_template('index.html', username=session['username'], birds=birds)
  else:
    return render_template('index.html', username=None)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3002, debug=True)
