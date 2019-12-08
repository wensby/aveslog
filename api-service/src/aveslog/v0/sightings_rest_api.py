from http import HTTPStatus
from typing import List

from flask import request, Response, make_response, jsonify, g

from aveslog.v0.models import Sighting
from aveslog.v0.models import Bird
from aveslog.v0.rest_api import require_authentication
from aveslog.v0.sighting import SightingRepository
from aveslog.v0.time import parse_date
from aveslog.v0.time import parse_time


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
    return make_response(jsonify(convert_sighting(sighting)), HTTPStatus.OK)
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
  g.database_session.add(sighting)
  g.database_session.commit()
  return post_sighting_success_response(sighting.id)


def sightings_response(sightings: List[Sighting], has_more: bool) -> Response:
  return make_response(jsonify({
    'items': list(map(convert_sighting, sightings)),
    'hasMore': has_more,
  }), HTTPStatus.OK)


def sightings_failure_response(error_message):
  return make_response(jsonify({
    'error': error_message,
  }), HTTPStatus.BAD_REQUEST)


def convert_sighting(sighting: Sighting) -> dict:
  result = {
    'id': sighting.id,
    'birderId': sighting.birder_id,
    'birdId': sighting.bird.binomial_name.lower().replace(' ', '-'),
    'date': sighting.sighting_date.isoformat(),
  }
  if sighting.sighting_time:
    result['time'] = sighting.sighting_time.isoformat()
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
