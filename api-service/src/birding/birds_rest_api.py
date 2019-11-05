import os
from http import HTTPStatus

from flask import Blueprint, make_response, jsonify, Response

from .bird_view import BirdViewFactory, BirdPageView
from .link import LinkFactory
from .picture import Picture


def create_birds_rest_api_blueprint(
      link_factory: LinkFactory,
      bird_view_factory: BirdViewFactory,
) -> Blueprint:
  blueprint = Blueprint('birds', __name__, url_prefix='/birds')

  @blueprint.route('/<string:binomial_name>')
  def get_bird(binomial_name: str) -> Response:
    reformatted = binomial_name.replace('-', ' ')
    view = bird_view_factory.create_bird_page_view(binomial_name=reformatted)
    return create_bird_response(view)

  @blueprint.route('/<int:bird_id>')
  def get_bird_by_id(bird_id: str) -> Response:
    view = bird_view_factory.create_bird_page_view(bird_id=bird_id)
    return create_bird_response(view)

  def create_bird_response(view: BirdPageView) -> Response:
    result = create_result(view)
    return make_response(jsonify({
      'status': 'success',
      'result': result,
    }), HTTPStatus.OK)

  def create_result(view: BirdPageView) -> dict:
    result = {'binomialName': view.bird.binomial_name}
    if view.cover_picture:
      result['coverUrl'] = external_picture_url(view.cover_picture)
    if view.thumbnail_picture:
      result['thumbnailCredit'] = view.thumbnail_picture.credit
      result['thumbnailUrl'] = external_picture_url(view.thumbnail_picture)
    return result

  def external_picture_url(picture: Picture) -> str:
    static_picture_url = os.path.join('/static/', picture.filepath)
    return link_factory.create_url_external_link(static_picture_url)

  return blueprint
