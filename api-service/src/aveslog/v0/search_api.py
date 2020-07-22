import os
from http import HTTPStatus
from operator import attrgetter

from flask import Response, request, current_app, make_response, jsonify, g

from aveslog.v0.birds_rest_api import bird_summary_representation
from aveslog.v0.link import LinkFactory
from aveslog.v0.models import Picture
from aveslog.v0.models import Sighting
from aveslog.v0.rest_api import optional_authentication
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
  if 'stats' in embed and hasattr(g, 'authenticated_account'):
    stats = {}
    sightings = g.database_session.query(Sighting) \
      .filter_by(birder_id=g.authenticated_account.birder.id) \
      .filter_by(bird_id=match.bird.id) \
      .order_by(Sighting.sighting_date.desc(), Sighting.sighting_time.desc()) \
      .all()
    if sightings:
      stats['lastSighting'] = sightings[0].sighting_date.isoformat()
    item['stats'] = stats
  return item


@optional_authentication
def search_birds() -> Response:
  query = request.args.get('q')
  page_size = parse_page_size(request.args)
  embed = parse_embed_list(request.args)
  bird_searcher = BirdSearcher(g.database_session)
  matches = bird_searcher.search(query)
  matches = sorted(matches, key=attrgetter('score'), reverse=True)[:page_size]
  return make_response(jsonify({
    'items': [_result_item(m, embed) for m in matches],
  }), HTTPStatus.OK)


def parse_page_size(args):
  request_page_size = args.get('page_size', type=int)
  return request_page_size if request_page_size else 30


def parse_embed_list(args):
  return args.get('embed', type=str).split(',') if 'embed' in args else []
