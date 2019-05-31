import os.path
import json

from flask import Blueprint
from flask import request
from flask import session
from flask import g
from datetime import datetime, timedelta
from .render import render_page
from .authentication import require_login
from .sighting import SightingPost

def create_sighting_blueprint(account_repo, sighting_repo, bird_repo):
  blueprint = Blueprint('sighting', __name__)

  @blueprint.route('/sighting', methods=['POST'])
  @require_login
  def post_sighting():
    sighting_post = create_sighting_post(request.form)
    result = sighting_repo.add_sighting(sighting_post)
    headers = {'ContentType':'application/json'}
    if 'INSERT 0 1' in result.status:
      return json.dumps({'success':True}), 201, headers
    else:
      return json.dumps({'success':False}), 400, headers
  
  def create_sighting_post(form):
    bird_id = int(form['bird_id'])
    timezoneoffset = int(form['timezoneoffset'])
    sighting_datetime = datetime.utcnow() + timedelta(minutes=timezoneoffset)
    person_id = g.logged_in_account.person_id
    date = sighting_datetime.date()
    time = sighting_datetime.time()
    return SightingPost(person_id, bird_id, date, time)

  def find_thumbnail_image(bird):
    birdname = bird.binomial_name.lower().replace(' ', '-')
    path = "image/bird/" + birdname + "-thumb.jpg"
    if os.path.isfile(blueprint.root_path + "/static/" + path):
      return path

  return blueprint
