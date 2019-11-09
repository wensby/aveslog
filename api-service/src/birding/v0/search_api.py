import os
from http import HTTPStatus

from .bird import BirdRepository
from birding.picture import PictureRepository
from birding.link import LinkFactory
from birding.picture import Picture
from birding.rest_api import RestApiResponse
from .search import BirdSearchMatch
from .search import BirdSearchController


class SearchApi:

  def __init__(self,
        controller: BirdSearchController,
        bird_repository: BirdRepository,
        picture_repository: PictureRepository,
        link_factory: LinkFactory,
  ):
    self.controller = controller
    self.bird_repository = bird_repository
    self.picture_repository = picture_repository
    self.link_factory = link_factory

  def result_item(self, match: BirdSearchMatch):
    item = {
      'id': match.bird.binomial_name.lower().replace(' ', '-'),
      'binomialName': match.bird.binomial_name,
      'score': match.score,
    }
    bird_thumbnail = self.bird_repository.bird_thumbnail(match.bird)
    if bird_thumbnail:
      item['thumbnail'] = self.get_bird_thumbnail_url(bird_thumbnail)
    return item

  def search_birds(self, query, limit):
    bird_matches = list(
      map(self.result_item, self.controller.search(query, limit)))
    return RestApiResponse(HTTPStatus.OK, {
      'items': bird_matches,
    })

  def get_bird_thumbnail_url(self, bird_thumbnail):
    pictures = self.picture_repository.pictures()
    picture = [x for x in pictures if x.id == bird_thumbnail.picture_id][0]
    return self.external_picture_url(picture)

  def external_picture_url(self, picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return self.link_factory.create_url_external_link(static_picture_url)
