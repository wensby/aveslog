import os.path
import re
from flask import Flask, request, redirect, url_for
app = Flask(__name__)

bird_filepath_str = '/data/bird.txt'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  if request.method == 'POST':
    bird = request.form['bird']
    if len(bird) < 20 and re.compile("^([A-z]+)( [A-z]+)*$").match(bird):
      with open(bird_filepath_str, 'a+') as f:
        f.write(bird + '\n')
    return redirect(url_for('hello_world'))
  else:
    form = '<form action="/" method="post">Bird:<input type="text" name="bird"></form><br>'
    if not os.path.exists(bird_filepath_str):
      open(bird_filepath_str, 'w+').close()
    with open(bird_filepath_str, 'r') as f:
      birds = [line.rstrip('\n') for line in f]
      return form + repr(birds)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3002)
