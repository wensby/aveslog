import os.path
import re
from pathlib import Path
from flask import Flask, request, redirect, url_for, session, render_template
from sighting import SightingRepository
from bird import BirdRepository
from person import PersonRepository
app = Flask(__name__)

bird_directory = '/data/'
app.secret_key = open('/app/secret_key', 'r').readline()
sighting_file = Path('/data/sighting/sighting.txt')
bird_file = Path('/data/bird/bird.txt')
person_file = Path('/data/person/person.txt')

bird_repo = BirdRepository(bird_file)
sighting_repo = SightingRepository(sighting_file)
person_repo = PersonRepository(person_file)

def login_username():
  username = request.form['username']
  if re.compile('^[A-z]{1,20}$').match(username):
    if not person_repo.containsname(username):
      person = person_repo.add_person(username)
      session['username'] = person.name
    else:
      person = person_repo.get_person_by_name(username)
      session['username'] = person.name

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    login_username()
    return redirect(url_for('index'))
  else:
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))

def get_bird_filepath_str(username):
  return bird_directory + username + '.txt'

def createbirdfileifnotpresent(username):
  bird_filepath_str = get_bird_filepath_str(session['username'])
  if not os.path.exists(bird_filepath_str):
    open(bird_filepath_str, 'w+').close()

def putbird(bird_name):
  if session['username']:
    person_name = session['username']
    person_id = person_repo.get_person_by_name(person_name).id
    bird = bird_repo.get_bird_by_name(bird_name)
    if not bird:
      bird = bird_repo.add_bird(bird_name)
    bird_id = bird.id
    sighting_repo.add_sighting(person_id, bird_id)

def getbirds():
  if session['username']:
    person_name = session['username']
    person_id = person_repo.get_person_by_name(person_name).id
    sightings = sighting_repo.get_sightings_by_person_id(person_id)
    birds = []
    for sighting in sightings:
      birds.append(bird_repo.get_bird_by_id(sighting.bird_id).name)
    return birds

@app.route('/', methods=['GET', 'POST'])
def index():
  if 'username' in session:
    if request.method == 'POST':
      bird = request.form['bird']
      putbird(bird)
      return redirect(url_for('index'))
    else:
      birds = getbirds()
      return render_template('home.html', username=session['username'], birds=birds)
  else:
    return redirect(url_for('login'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3002)
