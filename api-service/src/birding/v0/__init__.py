from http import HTTPStatus

from flask import Blueprint, make_response, jsonify

from .localization import LocaleLoader
from .localization import LocaleRepository
from birding.link import LinkFactory
from .search_api import SearchApi
from .bird import BirdRepository
from birding.picture import PictureRepository
from .birds_rest_api import BirdsRestApi
from .routes import create_birds_routes
from .routes import create_search_routes
from .search import StringMatcher
from .search import BirdSearcher


def create_api_v0_blueprint(
      link_factory: LinkFactory,
      bird_repository: BirdRepository,
      picture_repository: PictureRepository,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
) -> Blueprint:
  def register_routes(routes):
    for route in routes:
      rule = route['rule']
      endpoint = route.get('endpoint', None)
      view_func = route['view_func']
      options = route.get('options', {})
      blueprint.add_url_rule(rule, endpoint, view_func, **options)
      blueprint.add_url_rule(f'/v0{rule}', endpoint, view_func, **options)

  birds_rest_api = BirdsRestApi(
    link_factory,
    bird_repository,
    picture_repository,
  )
  string_matcher = StringMatcher()
  bird_searcher = BirdSearcher(
    bird_repository, locale_repository, string_matcher, locale_loader)

  search_api = SearchApi(
    bird_searcher,
    bird_repository,
    picture_repository,
    link_factory,
  )

  blueprint = Blueprint('v0', __name__)
  birds_routes = create_birds_routes(birds_rest_api)
  register_routes(birds_routes)
  search_routes = create_search_routes(search_api)
  register_routes(search_routes)

  @blueprint.app_errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
  def too_many_requests_handler(e):
    return make_response(jsonify({
      'error': f'rate limit exceeded {e.description}',
    }), HTTPStatus.TOO_MANY_REQUESTS)

  return blueprint
