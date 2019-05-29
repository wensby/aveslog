import os.path

from flask import Blueprint
from flask import request
from flask import session
from flask import g
from datetime import datetime, timedelta
from .render import render_page

def create_sighting_blueprint(account_repo, sighting_repo, bird_repo):
  blueprint = Blueprint('sighting', __name__)

  @blueprint.route('/sighting', methods=['POST'])
  def post_sighting():
    bird_id = int(request.form['bird_id'])
    timezoneoffset = int(request.form['timezoneoffset'])
    sighting_time = datetime.utcnow() + timedelta(minutes=timezoneoffset)
    putbird(bird_id, sighting_time)
    return 'success?'
  
  def putbird(bird_id, sighting_time):
    if g.logged_in_account:
      person_id = g.logged_in_account.person_id
      sighting_repo.add_sighting(person_id, bird_id, sighting_time)

  def find_thumbnail_image(bird):
    birdname = bird.binomial_name.lower().replace(' ', '-')
    path = "image/bird/" + birdname + "-thumb.jpg"
    if os.path.isfile(blueprint.root_path + "/static/" + path):
      return path

  return blueprint
