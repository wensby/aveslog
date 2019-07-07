from flask import Blueprint
from flask import request
from flask import g
from .render import render_page


def create_bird_blueprint(bird_view_factory, bird_search_controller,
      bird_search_view_factory):
  controller = bird_search_controller
  view_factory = bird_view_factory

  blueprint = Blueprint('bird', __name__, url_prefix='/bird')

  @blueprint.route('/')
  def get_bird():
    bird_id = int(request.args.get('bird_id'))
    view = view_factory.create_bird_page_view(bird_id)
    g.render_context['view'] = view
    return render_page('bird.html')

  @blueprint.route('/search')
  def search():
    name = request.args.get('query')
    bird_matches = controller.search(name)
    result_items = bird_search_view_factory.create_search_result_items(
      bird_matches)
    g.render_context['result_items'] = result_items
    return render_page('birdsearch.html')

  return blueprint
