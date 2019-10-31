import os
from http import HTTPStatus

from flask import Blueprint, make_response, jsonify, request

from .bird import BirdRepository
from .link import LinkFactory
from .picture import PictureRepository, Picture
from .search import BirdSearchController


def create_search_api_blueprint(
      controller: BirdSearchController,
      bird_repository: BirdRepository,
      picture_repository: PictureRepository,
      link_factory: LinkFactory,
) -> Blueprint:
  blueprint = Blueprint('search', __name__, url_prefix='/search')

  def result_item(bird):
    item = {
      'id': bird.id,
      'binomialName': bird.binomial_name,
    }
    bird_thumbnail = bird_repository.bird_thumbnail(bird)
    if bird_thumbnail:
      item['thumbnail'] = get_bird_thumbnail_url(bird_thumbnail)
    return item

  @blueprint.route('/birds')
  def search_birds():
    name = request.args.get('q')
    limit = request.args.get('limit', type=int)
    bird_matches = list(map(result_item, map(
      lambda match: match.bird, controller.search(name, limit))))
    return make_response(jsonify({
      'items': bird_matches,
    }), HTTPStatus.OK)

  def get_bird_thumbnail_url(bird_thumbnail):
    pictures = picture_repository.pictures()
    picture = [x for x in pictures if x.id == bird_thumbnail.picture_id][0]
    return external_picture_url(picture)

  def external_picture_url(picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return link_factory.create_url_external_link(static_picture_url)

  return blueprint
