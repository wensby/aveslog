import os
from http import HTTPStatus

from .bird import BirdRepository
from .birds_rest_api import bird_summary_representation
from birding.picture import PictureRepository
from birding.link import LinkFactory
from birding.picture import Picture
from birding.rest_api import RestApiResponse
from .search import BirdSearchMatch, BirdSearcher


class SearchApi:

  def __init__(self,
        bird_searcher: BirdSearcher,
        bird_repository: BirdRepository,
        picture_repository: PictureRepository,
        link_factory: LinkFactory,
  ):
    self.bird_searcher = bird_searcher
    self.bird_repository = bird_repository
    self.picture_repository = picture_repository
    self.link_factory = link_factory

  def search_birds(self,
        query: str,
        embed: list = None,
        page_size: int = 30,
  ) -> RestApiResponse:
    page_size = page_size if page_size else 30
    embed = embed if embed else []
    search_matches = self.bird_searcher.search(query)
    search_matches.sort(key=lambda m: m.score, reverse=True)
    bird_matches = list(
      map(lambda x: self._result_item(x, embed), search_matches[:page_size]))
    return RestApiResponse(HTTPStatus.OK, {
      'items': bird_matches,
    })

  def _result_item(self, match: BirdSearchMatch, embed: list) -> dict:
    bird = match.bird
    item = bird_summary_representation(bird)
    item['score'] = match.score
    if 'thumbnail' in embed and bird.thumbnail:
      item['thumbnail'] = {
        'url': self._external_picture_url(bird.thumbnail.picture),
        'credit': bird.thumbnail.picture.credit
      }
    return item

  def _external_picture_url(self, picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return self.link_factory.create_url_external_link(static_picture_url)
