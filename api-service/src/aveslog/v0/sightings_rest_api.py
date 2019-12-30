from datetime import datetime
from http import HTTPStatus
from typing import List

from flask import request, Response, make_response, jsonify, g, current_app
from geoalchemy2 import WKTElement

from aveslog.v0.geocoding import create_geocoding
from aveslog.v0.models import Sighting, PositionName, Locale
from aveslog.v0.models import Position
from aveslog.v0.models import Bird
from aveslog.v0.rest_api import require_authentication
from aveslog.v0.sighting import SightingRepository
from aveslog.v0.time import parse_date
from aveslog.v0.time import parse_time
from shapely import wkb


@require_authentication
def get_birder_sightings(birder_id: int):
  sighting_repository = SightingRepository()
  (sightings, total_rows) = sighting_repository.sightings(
    birder_id=birder_id)
  return sightings_response(sightings, False)


@require_authentication
def get_sightings():
  limit = request.args.get('limit', type=int)
  if limit is not None and limit <= 0:
    return sightings_failure_response('limit-invalid')
  sighting_repository = SightingRepository()
  (sightings, total_rows) = sighting_repository.sightings(limit=limit)
  has_more = total_rows > limit if limit is not None else False
  return sightings_response(sightings, has_more)


@require_authentication
def get_sighting(sighting_id: int) -> Response:
  account = g.authenticated_account
  sighting = g.database_session.query(Sighting).get(sighting_id)
  if sighting and sighting.birder_id == account.birder_id:
    return make_response(jsonify(sighting_representation(sighting)),
      HTTPStatus.OK)
  else:
    return get_sighting_failure_response()


@require_authentication
def delete_sighting(sighting_id: int) -> Response:
  account = g.authenticated_account
  sighting = g.database_session.query(Sighting).get(sighting_id)
  if not sighting:
    return sighting_deleted_response()
  if sighting.birder_id != account.birder_id:
    return sighting_delete_unauthorized_response()
  g.database_session.delete(sighting)
  g.database_session.commit()
  return sighting_deleted_response()


def create_position(lat, lon):
  element = WKTElement(f'POINT({lon} {lat})')
  return Position(point=element)


@require_authentication
def post_sighting() -> Response:
  account = g.authenticated_account
  birder_id = request.json['birder']['id']
  if account.birder_id != birder_id:
    return post_sighting_unauthorized_response()
  binomial_name = request.json['bird']['binomialName']
  bird = g.database_session.query(Bird).filter(
    Bird.binomial_name.ilike(binomial_name)).first()
  if not bird:
    return make_response('', HTTPStatus.BAD_REQUEST)
  sighting = create_sighting(request.json, bird)
  if 'position' in request.json:
    request_position = request.json['position']
    position = create_position(request_position['lat'], request_position['lon'])
    coordinates = (request_position['lat'], request_position['lon'])
    position_name = create_position_name(coordinates, g.database_session)
    if position_name:
      position.names.append(position_name)
    sighting.position = position
  g.database_session.add(sighting)
  g.database_session.commit()
  return post_sighting_success_response(sighting.id)


def create_position_name(coordinates, db_session):
  geocoding = create_geocoding(current_app.testing)
  reverse_geocoding_result = geocoding.reverse_search(coordinates)
  if reverse_geocoding_result:
    language_code = reverse_geocoding_result.language_code
    primary_language_subtag = language_code.split('-')[0]
    locale = db_session.query(Locale) \
      .filter_by(code=primary_language_subtag) \
      .first()
    if locale:
      position_name = PositionName(
        locale_id=locale.id,
        detail_level=reverse_geocoding_result.detail_level,
        name=reverse_geocoding_result.name,
        creation_time=datetime.now(),
      )
      position_name.locale = locale
      return position_name


def sightings_response(sightings: List[Sighting], has_more: bool) -> Response:
  return make_response(jsonify({
    'items': list(map(bird_summary_representation, sightings)),
    'hasMore': has_more,
  }), HTTPStatus.OK)


def sightings_failure_response(error_message):
  return make_response(jsonify({
    'error': error_message,
  }), HTTPStatus.BAD_REQUEST)


def bird_summary_representation(sighting: Sighting) -> dict:
  result = {
    'id': sighting.id,
    'birderId': sighting.birder_id,
    'birdId': sighting.bird.binomial_name.lower().replace(' ', '-'),
    'date': sighting.sighting_date.isoformat(),
  }
  if sighting.sighting_time:
    result['time'] = sighting.sighting_time.isoformat()
  if sighting.position:
    point = wkb.loads(bytes(sighting.position.point.data))
    result['position'] = {
      'lat': point.y,
      'lon': point.x,
    }
  return result


def sighting_representation(sighting: Sighting) -> dict:
  result = {
    'id': sighting.id,
    'birderId': sighting.birder_id,
    'birdId': sighting.bird.binomial_name.lower().replace(' ', '-'),
    'date': sighting.sighting_date.isoformat(),
  }
  if sighting.sighting_time:
    result['time'] = sighting.sighting_time.isoformat()
  position = sighting.position
  if position:
    point = wkb.loads(bytes(position.point.data))
    result['position'] = {
      'lat': point.y,
      'lon': point.x,
    }
    if position.names:
      result['position']['name'] = sighting.position.names[0].name
  return result


def get_sighting_failure_response() -> Response:
  return make_response(jsonify({
    'status': 'failure',
    'message': 'You are not authorized to get this sighting'
  }), HTTPStatus.UNAUTHORIZED)


def sighting_deleted_response() -> Response:
  return make_response('', HTTPStatus.NO_CONTENT)


def sighting_delete_unauthorized_response() -> Response:
  return make_response('', HTTPStatus.UNAUTHORIZED)


def create_sighting(post_data: dict, bird: Bird) -> Sighting:
  return Sighting(
    birder_id=post_data['birder']['id'], bird_id=bird.id,
    sighting_date=parse_date(post_data['date']),
    sighting_time=parse_time(
      post_data['time']) if 'time' in post_data else None)


def post_sighting_success_response(sighting_id: int) -> Response:
  response = make_response(jsonify({
    'status': 'success',
  }), HTTPStatus.CREATED)
  response.headers['Location'] = f'/sightings/{sighting_id}'
  response.autocorrect_location_header = False
  return response


def post_sighting_unauthorized_response() -> Response:
  return make_response(jsonify({
    'status': 'failure',
  }), HTTPStatus.UNAUTHORIZED)
