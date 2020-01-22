import os
from http import HTTPStatus

from flask import Response, request, current_app, make_response, jsonify, g

from aveslog.v0.birds_rest_api import bird_summary_representation
from aveslog.v0.link import LinkFactory
from aveslog.v0.models import Picture
from aveslog.v0.search import BirdSearchMatch
from aveslog.v0.search import BirdSearcher


def _external_picture_url(picture: Picture) -> str:
  static_picture_url = os.path.join('/static/', picture.filepath)
  link_factory = LinkFactory(
    current_app.config['EXTERNAL_HOST'],
    current_app.config['FRONTEND_HOST'],
  )
  return link_factory.create_url_external_link(static_picture_url)


def _result_item(match: BirdSearchMatch, embed: list) -> dict:
  bird = match.bird
  item = bird_summary_representation(bird)
  item['score'] = match.score
  if 'thumbnail' in embed and bird.thumbnail:
    item['thumbnail'] = {
      'url': _external_picture_url(bird.thumbnail.picture),
      'credit': bird.thumbnail.picture.credit
    }
  return item


def search_birds() -> Response:
  query = request.args.get('q')
  page_size = request.args.get('page_size', type=int)
  embed = parse_embed_list(request.args)
  page_size = page_size if page_size else 30
  embed = embed if embed else []
  bird_searcher = BirdSearcher(g.database_session)
  search_matches = bird_searcher.search(query)
  search_matches.sort(key=lambda m: m.score, reverse=True)
  bird_matches = list(
    map(lambda x: _result_item(x, embed), search_matches[:page_size]))
  return make_response(jsonify({
    'items': bird_matches,
  }), HTTPStatus.OK)


def parse_embed_list(args):
  return args.get('embed', type=str).split(',') if 'embed' in args else []
