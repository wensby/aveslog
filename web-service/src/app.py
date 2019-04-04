import os.path
import re
from flask import Flask, request, redirect, url_for, session, render_template
app = Flask(__name__)

bird_filepath_str = '/data/bird.txt'
app.secret_key = '40958hft09834utnv093nt50934tv983vnu4'

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('index'))

def putbird(bird):
  if len(bird) < 20 and re.compile("^([A-z]+)( [A-z]+)*$").match(bird):
    with open(bird_filepath_str, 'a+') as f:
      f.write(bird + '\n')

def getbirds():
  if not os.path.exists(bird_filepath_str):
    open(bird_filepath_str, 'w+').close()
  with open(bird_filepath_str, 'r') as f:
    return [line.rstrip('\n') for line in f]

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
