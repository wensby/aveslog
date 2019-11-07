from flask import Response

from birding.birds_rest_api import BirdsRestApi, create_flask_response


def create_birds_routes(birds_rest_api: BirdsRestApi):
  def get_bird(binomial_name: str) -> Response:
    response = birds_rest_api.get_bird(binomial_name)
    return create_flask_response(response)

  def get_bird_by_id(bird_id: str) -> Response:
    response = birds_rest_api.get_bird(bird_id)
    return create_flask_response(response)

  routes = [{
    'rule': '/birds/<string:binomial_name>',
    'view_func': get_bird,
  }, {
    'rule': '/birds/<int:bird_id>',
    'view_func': get_bird_by_id,
  }]

  return routes
