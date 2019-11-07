import os
from http import HTTPStatus

from flask import make_response, jsonify, Response

from .bird import BirdRepository
from .rest_api import RestApiResponse
from .link import LinkFactory
from .picture import Picture, PictureRepository


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
    bird = self.get_bird_data(binomial_name=reformatted)
    return RestApiResponse(HTTPStatus.OK, bird)

  def get_bird_data(self, binomial_name=None) -> dict:
    bird = self.bird_repository.get_bird_by_binomial_name(binomial_name)
    thumbnail_picture = self.get_thumbnail(bird)
    cover_picture = thumbnail_picture
    bird_data = {
      'id': bird.binomial_name.lower().replace(' ', '-'),
      'binomialName': bird.binomial_name,
    }
    if cover_picture:
      bird_data['coverUrl'] = self.external_picture_url(cover_picture)
    if thumbnail_picture:
      bird_data['thumbnailCredit'] = thumbnail_picture.credit
      bird_data['thumbnailUrl'] = self.external_picture_url(thumbnail_picture)
    return bird_data

  def get_thumbnail(self, bird):
    thumbnail = self.bird_repository.bird_thumbnail(bird)
    if thumbnail:
      pictures = self.picture_repository.pictures()
      return [x for x in pictures if x.id == thumbnail.picture_id][0]

  def external_picture_url(self, picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return self.link_factory.create_url_external_link(static_picture_url)


def create_flask_response(response: RestApiResponse) -> Response:
  return make_response(jsonify(response.data), response.status)
