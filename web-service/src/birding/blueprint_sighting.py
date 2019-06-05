import os.path
import json

from flask import Blueprint
from flask import request
from flask import g
from .blueprint_authentication import require_login
from .sighting import SightingPost
from .time import get_current_time
from .render import render_page

def create_sighting_blueprint(sighting_repository, sighting_view_factory):
  view_factory = sighting_view_factory

  blueprint = Blueprint('sighting', __name__, url_prefix='/sighting')

  @blueprint.route('/')
  @require_login
  def get_sightings_index():
    person_id = g.logged_in_account.person_id
    sightings = sighting_repository.get_sightings_by_person_id(person_id)
    g.render_context['sightings'] = view_factory.create_sighting_items(sightings)
    return render_page('sightings.html')

  @blueprint.route('/', methods=['POST'])
  @require_login
  def post_sighting():
    sighting_post = create_sighting_post(request.form)
    if sighting_repository.add_sighting(sighting_post):
      return create_post_sighting_response(True, 201)
    else:
      return create_post_sighting_response(False, 400)

  def create_post_sighting_response(success, status_code):
    headers = {'ContentType':'application/json'}
    return json.dumps({'success':success}), status_code, headers
  
  def create_sighting_post(form):
    bird_id = int(form['bird_id'])
    timezoneoffset_minute = int(form['timezoneoffset_minute'])
    sighting_datetime = get_current_time(timezoneoffset_minute)
    person_id = g.logged_in_account.person_id
    date = sighting_datetime.date()
    time = sighting_datetime.time()
    return SightingPost(person_id, bird_id, date, time)

  return blueprint
