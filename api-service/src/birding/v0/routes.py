from flask import Response

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
