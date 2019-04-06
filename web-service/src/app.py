import os.path
import re
from flask import Flask, request, redirect, url_for, session, render_template
app = Flask(__name__)

bird_directory = '/data/'
app.secret_key = '40958hft09834utnv093nt50934tv983vnasdfu4'

def login_username():
  username = request.form['username']
  if re.compile('^[A-z]{1,20}$').match(username):
    session['username'] = username

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

def get_bird_firepath_str(username):
  return bird_directory + username + '.txt'

def createbirdfileifnotpresent(username):
  bird_filepath_str = get_bird_firepath_str(session['username'])
  if not os.path.exists(bird_filepath_str):
    open(bird_filepath_str, 'w+').close()

def putbird(bird):
  if session['username']:
    bird_filepath_str = get_bird_firepath_str(session['username'])
    createbirdfileifnotpresent(session['username'])
    if re.compile("^[A-zåäöÅÄÖ ]{1,20}$").match(bird):
      with open(bird_filepath_str, 'a+') as f:
        f.write(bird + '\n')

def getbirds():
  if session['username']:
    bird_filepath_str = get_bird_firepath_str(session['username'])
    createbirdfileifnotpresent(session['username'])
    with open(bird_filepath_str, 'r') as f:
      return [line.rstrip('\n') for line in f]
  else:
    return []

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
