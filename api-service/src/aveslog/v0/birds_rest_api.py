from http import HTTPStatus

from flask import Response, make_response, jsonify, g
from sqlalchemy.orm import joinedload

from aveslog.v0.rest_api import cache
from .models import Bird
from .models import Sighting
from .models import Birder
from .models import BirdThumbnail


@cache(max_age=300)
def get_single_bird(bird_identifier: str) -> Response:
  binomial_name = (bird_identifier.replace('-', ' ').capitalize())
  bird = g.database_session.query(Bird) \
    .options(joinedload(Bird.names)) \
    .options(joinedload(Bird.thumbnail)
    .options(joinedload(BirdThumbnail.picture))) \
    .filter_by(binomial_name=binomial_name) \
    .first()
  if not bird:
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response(jsonify(bird_representation(bird)), HTTPStatus.OK)


def get_bird_statistics(bird_identifier: str) -> Response:
  name = bird_identifier.replace('-', ' ').capitalize()
  bird = g.database_session.query(Bird).filter_by(binomial_name=name).first()
  if not bird:
    return make_response('', HTTPStatus.NOT_FOUND)
  sightings_count = g.database_session.query(Sighting) \
    .filter_by(bird=bird) \
    .count()
  birders_count = g.database_session.query(Birder) \
    .filter(Birder.sightings.any(Sighting.bird == bird)) \
    .count()
  statistics = {
    'sightingsCount': sightings_count,
    'birdersCount': birders_count,
  }
  return make_response(jsonify(statistics), HTTPStatus.OK)


def bird_summary_representation(bird: Bird) -> dict:
  return {
    'id': bird.binomial_name.lower().replace(' ', '-'),
    'binomialName': bird.binomial_name,
  }


def bird_representation(bird: Bird) -> dict:
  representation = bird_summary_representation(bird)
  if bird.names:
    representation['commonNames'] = collect_bird_names(bird.names)
  if bird.thumbnail:
    thumbnail_representation = {
      'url': bird.thumbnail.picture.filepath,
      'credit': bird.thumbnail.picture.credit,
    }
    representation['thumbnail'] = thumbnail_representation
    representation['cover'] = thumbnail_representation
  return representation


def collect_bird_names(bird_names):
  names_by_locale_code = {}
  for bird_name in bird_names:
    code = bird_name.locale.code
    name = bird_name.name
    if code not in names_by_locale_code:
      names_by_locale_code[code] = []
    names_by_locale_code[code].append(name)
  return names_by_locale_code
