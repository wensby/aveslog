from flask import Blueprint
from flask import request
from flask import g
from flask import session
from .render import render_page

def create_search_blueprint(bird_searcher, bird_repository):
  blueprint = Blueprint('search', __name__)

  @blueprint.route('/bird/search')
  def bird_search():
    name = request.args.get('query')
    g.render_context['bird_matches'] = bird_searcher.search(name)
    g.render_context['bird_thumbnails'] = bird_repository.bird_thumbnails()
    return render_page('birdsearch.html')
  
  return blueprint
