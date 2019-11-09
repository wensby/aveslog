import os
from http import HTTPStatus

from flask import make_response, jsonify, Response

from .bird import BirdRepository, Bird
from birding.rest_api import RestApiResponse
from birding.link import LinkFactory
from birding.picture import Picture, PictureRepository


class BirdsRestApi:

  def __init__(self,
        link_factory: LinkFactory,
        bird_repository: BirdRepository,
        picture_repository: PictureRepository,
  ):
    self.link_factory = link_factory
    self.bird_repository = bird_repository
    self.picture_repository = picture_repository

  def get_bird(self, bird_identifier: str) -> RestApiResponse:
    if not isinstance(bird_identifier, str):
      raise Exception(f'Unexpected bird identifier: {bird_identifier}')
    reformatted = bird_identifier.replace('-', ' ')
    bird = self.bird_repository.get_bird_by_binomial_name(reformatted)
    if not bird:
      return RestApiResponse(HTTPStatus.NOT_FOUND, {'message': 'Not Found'})
    bird_data = self.get_bird_data(bird)
    return RestApiResponse(HTTPStatus.OK, bird_data)

  def get_bird_data(self, bird: Bird) -> dict:
    bird_data = {
      'id': bird.binomial_name.lower().replace(' ', '-'),
      'binomialName': bird.binomial_name,
    }
    if bird.thumbnail:
      bird_data['thumbnail'] = {
        'url': self.external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit,
      }
    if bird.thumbnail:
      bird_data['cover'] = {
        'url': self.external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit,
      }
    return bird_data

  def external_picture_url(self, picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return self.link_factory.create_url_external_link(static_picture_url)


def create_flask_response(response: RestApiResponse) -> Response:
  return make_response(jsonify(response.data), response.status)
