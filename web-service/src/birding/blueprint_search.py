from flask import Blueprint
from flask import request
from flask import g
from flask import session
from .render import render_page

def create_search_blueprint(bird_searcher, bird_search_view_factory):
  view_factory = bird_search_view_factory

  blueprint = Blueprint('search', __name__)

  @blueprint.route('/bird/search')
  def bird_search():
    name = request.args.get('query')
    bird_matches = bird_searcher.search(name)[:100]
    result_items = view_factory.create_search_result_items(bird_matches)
    g.render_context['result_items'] = result_items
    return render_page('birdsearch.html')
  
  return blueprint
