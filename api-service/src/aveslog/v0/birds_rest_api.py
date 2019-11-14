import os
from http import HTTPStatus

from .bird import BirdRepository
from .models import Bird, Picture
from .rest_api import RestApiResponse
from .link import LinkFactory


class BirdsRestApi:

  def __init__(self,
        link_factory: LinkFactory,
        bird_repository: BirdRepository,
  ):
    self._link_factory = link_factory
    self._bird_repository = bird_repository

  def get_bird(self, bird_identifier: str) -> RestApiResponse:
    if not isinstance(bird_identifier, str):
      raise Exception(f'Unexpected bird identifier: {bird_identifier}')
    reformatted = bird_identifier.replace('-', ' ')
    bird = self._bird_repository.get_bird_by_binomial_name(reformatted)
    if not bird:
      return RestApiResponse(HTTPStatus.NOT_FOUND, {'message': 'Not Found'})
    bird_data = self._get_bird_data(bird)
    return RestApiResponse(HTTPStatus.OK, bird_data)

  def _get_bird_data(self, bird: Bird) -> dict:
    bird_data = {
      'id': bird.binomial_name.lower().replace(' ', '-'),
      'binomialName': bird.binomial_name,
    }
    if bird.thumbnail:
      bird_data['thumbnail'] = {
        'url': self._external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit,
      }
    if bird.thumbnail:
      bird_data['cover'] = {
        'url': self._external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit,
      }
    return bird_data

  def _external_picture_url(self, picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return self._link_factory.create_url_external_link(static_picture_url)


def bird_summary_representation(bird: Bird) -> dict:
  return {
    'id': bird.binomial_name.lower().replace(' ', '-'),
    'binomialName': bird.binomial_name,
  }
