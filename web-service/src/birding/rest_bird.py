from http import HTTPStatus

from flask import Blueprint, make_response, jsonify, request

from .search import BirdSearchController, BirdMatch


def create_v2_bird_blueprint(
      controller: BirdSearchController,
) -> Blueprint:
  blueprint = Blueprint('v2bird', __name__,
                        url_prefix='/v2/bird')

  def result_item(match):
    return {
      'birdId': match.bird.id,
      'binomialName': match.bird.binomial_name,
    }

  @blueprint.route('')
  def query_birds():
    name = request.args.get('q')
    bird_matches = list(map(result_item, controller.search(name)))
    return make_response(jsonify({
      'status': 'success',
      'result': bird_matches,
    }), HTTPStatus.OK)

  return blueprint
