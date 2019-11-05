import os
from http import HTTPStatus

from flask import Blueprint, make_response, jsonify, Response

from .bird_resource import BirdResourceAccessor, BirdResource
from .link import LinkFactory
from .picture import Picture


def create_birds_rest_api_blueprint(
      link_factory: LinkFactory,
      bird_resource_accessor: BirdResourceAccessor,
) -> Blueprint:
  blueprint = Blueprint('birds', __name__, url_prefix='/birds')

  @blueprint.route('/<string:binomial_name>')
  def get_bird(binomial_name: str) -> Response:
    reformatted = binomial_name.replace('-', ' ')
    bird = bird_resource_accessor.access_bird(binomial_name=reformatted)
    return create_bird_response(bird)

  @blueprint.route('/<int:bird_id>')
  def get_bird_by_id(bird_id: str) -> Response:
    bird = bird_resource_accessor.access_bird(bird_id=bird_id)
    return create_bird_response(bird)

  def create_bird_response(bird: BirdResource) -> Response:
    result = create_result(bird)
    return make_response(jsonify({
      'status': 'success',
      'result': result,
    }), HTTPStatus.OK)

  def create_result(bird: BirdResource) -> dict:
    result = {'binomialName': bird.bird.binomial_name}
    if bird.cover_picture:
      result['coverUrl'] = external_picture_url(bird.cover_picture)
    if bird.thumbnail_picture:
      result['thumbnailCredit'] = bird.thumbnail_picture.credit
      result['thumbnailUrl'] = external_picture_url(bird.thumbnail_picture)
    return result

  def external_picture_url(picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return link_factory.create_url_external_link(static_picture_url)

  return blueprint
