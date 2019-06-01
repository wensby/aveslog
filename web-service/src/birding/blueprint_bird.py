from flask import Blueprint
from flask import request
from flask import g
from .render import render_page

def create_bird_blueprint(bird_repository, picture_repository):
  blueprint = Blueprint('bird', __name__, url_prefix='/bird')

  @blueprint.route('/')
  def get_bird():
    bird_id = int(request.args.get('bird_id'))
    bird = bird_repository.get_bird_by_id(bird_id)
    g.render_context['bird'] = bird
    g.render_context['thumbnail_photographer'] = get_thumbnail_credit(bird)
    return render_page('bird.html')

  def get_thumbnail_credit(bird):
    thumbnail = bird_repository.bird_thumbnail(bird)
    if thumbnail:
      pictures = picture_repository.pictures()
      return [x for x in pictures if x.id == thumbnail.picture_id][0].credit

  return blueprint
