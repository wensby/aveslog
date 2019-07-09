from flask import Blueprint
from flask import url_for
from flask import request
from flask import redirect
from flask import g
from .authentication_blueprint import require_login
from .sighting import SightingPost
from .time import parse_date
from .time import parse_time
from .render import render_page


def create_sighting_blueprint(sighting_repository, sighting_view_factory):
  view_factory = sighting_view_factory

  blueprint = Blueprint('sighting', __name__, url_prefix='/sighting')

  @blueprint.route('/')
  @require_login
  def get_sightings():
    items = view_factory.create_sighting_items(g.logged_in_account)
    g.render_context['sightings'] = items
    return render_page('sighting/sightings.html')

  @blueprint.route('/', methods=['POST'])
  @require_login
  def post_sighting():
    sighting_post = create_sighting_post(request.form)
    if sighting_repository.add_sighting(sighting_post):
      return redirect(url_for('sighting.get_sightings'))
    else:
      return redirect(url_for('sighting.get_sightings'))

  @blueprint.route('/create/<birdid>')
  @require_login
  def create(birdid):
    view = view_factory.create_sighting_creation_view(birdid)
    g.render_context['view'] = view
    return render_page('sighting/create.html')

  @blueprint.route('/<sighting_id>')
  @require_login
  def get_sighting(sighting_id):
    sighting = sighting_repository.find_sighting(sighting_id)
    if sighting and sighting.person_id == g.logged_in_account.person_id:
      g.render_context['sighting_view'] = view_factory.create_sighting_view(
        sighting)
      return render_page('sighting/sighting.html')
    else:
      return redirect(url_for('index'))

  @blueprint.route('/<sighting_id>', methods=['POST'])
  @require_login
  def post_sighting_edit(sighting_id):
    sighting = sighting_repository.find_sighting(sighting_id)
    if sighting and sighting.person_id == g.logged_in_account.person_id:
      if request.form['action'] == 'Delete':
        sighting_repository.delete_sighting(sighting_id)
        return redirect(url_for('sighting.get_sightings'))
    return redirect(url_for('index'))

  def create_sighting_post(form):
    bird_id = int(form['birdId'])
    person_id = g.logged_in_account.person_id
    date = parse_date(form['dateInput'])
    time = parse_time(
      form['timeTimeInput']) if 'timeTimeInput' in form else None
    return SightingPost(person_id, bird_id, date, time)

  return blueprint
