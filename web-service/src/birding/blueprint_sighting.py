import os.path
import json

from flask import Blueprint
from flask import request
from flask import g
from .authentication import require_login
from .sighting import SightingPost
from .time import get_current_time
from .render import render_page

def create_sighting_blueprint(sighting_repository, bird_repository, picture_repository):
  blueprint = Blueprint('sighting', __name__, url_prefix='/sighting')

  @blueprint.route('/')
  @require_login
  def get_sightings_index():
    sightings = get_sightings(g.logged_in_account)
    g.render_context['sightings'] = sightings
    return render_page('sightings.html')

  @blueprint.route('/', methods=['POST'])
  @require_login
  def post_sighting():
    sighting_post = create_sighting_post(request.form)
    if sighting_repository.add_sighting(sighting_post):
      return create_post_sighting_response(True, 201)
    else:
      return create_post_sighting_response(False, 400)

  def get_sightings(account):
    person_id = account.person_id
    sightings = sighting_repository.get_sightings_by_person_id(person_id)
    thumbnails = bird_repository.bird_thumbnails()
    pictures = picture_repository.pictures()
    result = []
    for sighting in sightings:
      bird = bird_repository.get_bird_by_id(sighting.bird_id)
      if bird:
        s = dict()
        sighting_time = sighting.sighting_date.isoformat()
        if sighting.sighting_time:
          sighting_time = sighting_time + ' ' + sighting.sighting_time.isoformat()
        s['bird'] = bird
        s['time'] = sighting_time
        thumbnail_image = find_thumbnail_image(bird, thumbnails, pictures)
        if thumbnail_image:
          s['thumbnail'] = thumbnail_image
        result.append(s)
    result.sort(reverse=True, key=lambda r: r['time'])
    return result

  def find_thumbnail_image(bird, thumbnails, pictures):
    thumbnail = [x for x in thumbnails if x.bird_id == bird.id]
    if len(thumbnail) < 1:
      return
    thumbnail = thumbnail[0]
    path = [x for x in pictures if x.id == thumbnail.picture_id][0].filepath
    if os.path.isfile(blueprint.root_path + "/static/" + path):
      return path

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
