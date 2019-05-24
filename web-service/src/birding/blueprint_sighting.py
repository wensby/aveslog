from flask import Blueprint
from flask import request
from flask import session
from flask import g
from datetime import datetime, timedelta
from .render import render_page

def create_sighting_blueprint(account_repo, sighting_repo, bird_repo):
  blueprint = Blueprint('sighting', __name__)

  def get_account(id):
    return account_repo.get_user_account_by_id(id)

  @blueprint.route('/sighting', methods=['POST'])
  def post_sighting():
    bird_id = int(request.form['bird_id'])
    timezoneoffset = int(request.form['timezoneoffset'])
    sighting_time = datetime.utcnow() + timedelta(minutes=timezoneoffset)
    putbird(bird_id, sighting_time)
    return 'success?'
  
  def putbird(bird_id, sighting_time):
    if 'account_id' in session:
      person_id = get_account(session['account_id']).person_id
      sighting_repo.add_sighting(person_id, bird_id, sighting_time)
  
  def get_sightings():
    if 'account_id' in session:
      person_id = get_account(session['account_id']).person_id
      sightings = sighting_repo.get_sightings_by_person_id(person_id)
      result = []
      for sighting in sightings:
        bird = bird_repo.get_bird_by_id(sighting.bird_id)
        if bird:
          sighting_time = sighting.sighting_date.isoformat()
          if sighting.sighting_time:
            sighting_time = sighting_time + ' ' + sighting.sighting_time.isoformat()
          result.append({'bird': bird, 'time': sighting_time})
      result.sort(reverse=True, key=lambda r: r['time'])
      return result

  @blueprint.route('/')
  def index():
    if 'account_id' in session:
      sightings = get_sightings()
      g.render_context['username'] = get_account(session['account_id']).username
      g.render_context['sightings'] = sightings
      return render_page('index.html')
    else:
      return render_page('index.html')

  return blueprint
