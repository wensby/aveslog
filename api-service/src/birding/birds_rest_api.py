import os
from http import HTTPStatus
from typing import Union

from flask import Blueprint, make_response, jsonify, Response

from .rest_api import RestApiResponse
from .bird_resource import BirdResourceAccessor, BirdResource
from .link import LinkFactory
from .picture import Picture


class BirdsRestApi:

  def __init__(self,
        bird_resource_accessor: BirdResourceAccessor,
        link_factory: LinkFactory,
  ):
    self.bird_resource_accessor = bird_resource_accessor
    self.link_factory = link_factory

  def get_bird(self, bird_identifier: Union[int, str]) -> RestApiResponse:
    if not isinstance(bird_identifier, (int, str)):
      raise Exception(f'Unexpected bird identifier: {bird_identifier}')
    if isinstance(bird_identifier, str):
      reformatted = bird_identifier.replace('-', ' ')
      bird_identifier = self.bird_resource_accessor.access_bird(
        binomial_name=reformatted)
    else:
      bird_identifier = self.bird_resource_accessor.access_bird(
        bird_id=bird_identifier)
    return RestApiResponse(HTTPStatus.OK, {
      'status': 'success',
      'result': self.create_result(bird_identifier),
    })

  def create_result(self, bird: BirdResource) -> dict:
    result = {'binomialName': bird.bird.binomial_name}
    if bird.cover_picture:
      result['coverUrl'] = self.external_picture_url(bird.cover_picture)
    if bird.thumbnail_picture:
      result['thumbnailCredit'] = bird.thumbnail_picture.credit
      result['thumbnailUrl'] = self.external_picture_url(bird.thumbnail_picture)
    return result

  def external_picture_url(self, picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return self.link_factory.create_url_external_link(static_picture_url)


def create_flask_response(response: RestApiResponse) -> Response:
  return make_response(jsonify(response.data), response.status)


def create_birds_rest_api_blueprint(birds_rest_api: BirdsRestApi) -> Blueprint:
  blueprint = Blueprint('birds', __name__, url_prefix='/birds')

  @blueprint.route('/<string:binomial_name>')
  def get_bird(binomial_name: str) -> Response:
    response = birds_rest_api.get_bird(binomial_name)
    return create_flask_response(response)

  @blueprint.route('/<int:bird_id>')
  def get_bird_by_id(bird_id: str) -> Response:
    response = birds_rest_api.get_bird(bird_id)
    return create_flask_response(response)

  return blueprint
