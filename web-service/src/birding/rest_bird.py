import os
from http import HTTPStatus

from flask import Blueprint, make_response, jsonify, request

from .search import BirdSearchController, BirdMatch
from .link import LinkFactory
from .picture import PictureRepository
from .bird import BirdRepository


def create_v2_bird_blueprint(
      controller: BirdSearchController,
      bird_repository: BirdRepository,
      picture_repository: PictureRepository,
      link_factory: LinkFactory,
) -> Blueprint:
  blueprint = Blueprint('v2bird', __name__,
                        url_prefix='/v2/bird')

  def result_item(match):
    item = {
      'birdId': match.bird.id,
      'binomialName': match.bird.binomial_name,
    }
    bird_thumbnail = bird_repository.bird_thumbnail(match.bird)
    if bird_thumbnail:
      item['thumbnail'] = get_bird_thumbnail_url(bird_thumbnail)
    return item

  @blueprint.route('')
  def query_birds():
    name = request.args.get('q')
    bird_matches = list(map(result_item, controller.search(name)))
    return make_response(jsonify({
      'status': 'success',
      'result': bird_matches,
    }), HTTPStatus.OK)

  def get_bird_thumbnail_url(bird_thumbnail):
    pictures = picture_repository.pictures()
    picture = [x for x in pictures if x.id == bird_thumbnail.picture_id][0]
    static_picture_url = os.path.join('/static/', picture.filepath)
    return link_factory.create_url_external_link(static_picture_url)

  return blueprint
