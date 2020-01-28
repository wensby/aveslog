from http import HTTPStatus

from flask import Response, make_response, jsonify, g, request
from sqlalchemy.orm import joinedload

from aveslog.v0.error import ErrorCode
from aveslog.v0.rest_api import validation_failed_error_response
from aveslog.v0.rest_api import cache
from aveslog.v0.rest_api import require_authentication
from aveslog.v0.rest_api import require_permission
from .models import Bird, BirdCommonName, Locale
from .models import Sighting
from .models import Birder
from .models import BirdThumbnail


@cache(max_age=300)
def get_single_bird(bird_identifier: str) -> Response:
  binomial_name = (bird_identifier.replace('-', ' ').capitalize())
  bird = g.database_session.query(Bird) \
    .options(joinedload(Bird.common_names)) \
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


@cache(max_age=300)
def get_common_names(bird_identifier: str) -> Response:
  binomial_name = bird_identifier.replace('-', ' ').capitalize()
  bird = g.database_session.query(Bird). \
    filter_by(binomial_name=binomial_name).first()
  if not bird:
    return make_response('', HTTPStatus.NOT_FOUND)
  common_names = bird.common_names
  json = jsonify({
    'items': list(map(common_name_representation, common_names))
  })
  return make_response(json, HTTPStatus.OK)


@cache(max_age=300)
def get_common_name(bird_identifier: str, id: int) -> Response:
  binomial_name = bird_identifier.replace('-', ' ').capitalize()
  common_name = g.database_session.query(BirdCommonName) \
    .join(BirdCommonName.bird) \
    .filter(Bird.binomial_name == binomial_name) \
    .filter(BirdCommonName.id == id) \
    .first()
  if not common_name:
    return make_response('', HTTPStatus.NOT_FOUND)
  json = jsonify(common_name_representation(common_name))
  return make_response(json, HTTPStatus.OK)


@require_authentication
@require_permission
def post_common_name(bird_identifier: str) -> Response:
  binomial_name = bird_identifier.replace('-', ' ').capitalize()
  bird = g.database_session.query(Bird). \
    filter_by(binomial_name=binomial_name).first()
  if not bird:
    return make_response('', HTTPStatus.NOT_FOUND)
  locale_code = request.json['locale']
  name = request.json['name']
  locale = g.database_session.query(Locale).filter_by(code=locale_code).first()
  if not locale:
    errors = [{
      'code': ErrorCode.INVALID_LOCALE_CODE,
      'field': 'locale_code',
      'message': 'Locale code not one of the valid options',
    }]
    return validation_failed_error_response(errors)
  common_name = BirdCommonName(locale_id=locale.id, name=name)
  bird.common_names.append(common_name)
  g.database_session.commit()
  response = make_response(jsonify({}), HTTPStatus.CREATED)
  response.headers[
    'Location'] = f'/birds/{bird_identifier}/common-names/{common_name.id}'
  response.autocorrect_location_header = False
  return response


def bird_summary_representation(bird: Bird) -> dict:
  return {
    'id': bird.binomial_name.lower().replace(' ', '-'),
    'binomialName': bird.binomial_name,
  }


def bird_representation(bird: Bird) -> dict:
  representation = bird_summary_representation(bird)
  if bird.common_names:
    representation['commonNames'] = collect_common_names(bird.common_names)
  if bird.thumbnail:
    thumbnail_representation = {
      'url': bird.thumbnail.picture.filepath,
      'credit': bird.thumbnail.picture.credit,
    }
    representation['thumbnail'] = thumbnail_representation
    representation['cover'] = thumbnail_representation
  return representation


def collect_common_names(common_names):
  names_by_locale_code = {}
  for common_name in common_names:
    code = common_name.locale.code
    name = common_name.name
    if code not in names_by_locale_code:
      names_by_locale_code[code] = []
    names_by_locale_code[code].append(name)
  return names_by_locale_code


def common_name_representation(common_name: BirdCommonName):
  return {
    'id': common_name.id,
    'locale': common_name.locale.code,
    'name': common_name.name,
  }
