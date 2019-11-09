from flask import Response, request

from .search_api import SearchApi
from .birds_rest_api import BirdsRestApi, create_flask_response


def create_birds_routes(birds_rest_api: BirdsRestApi):
  def get_bird(bird_identifier: str) -> Response:
    response = birds_rest_api.get_bird(bird_identifier)
    return create_flask_response(response)

  routes = [
    {
      'rule': '/birds/<string:bird_identifier>',
      'view_func': get_bird,
    },
  ]

  return routes


def create_search_routes(search_api: SearchApi):
  def search_birds() -> Response:
    query = request.args.get('q')
    limit = request.args.get('limit', type=int)
    response = search_api.search_birds(query, limit)
    return create_flask_response(response)

  return [
    {
      'rule': '/search/birds',
      'view_func': search_birds,
    }
  ]
