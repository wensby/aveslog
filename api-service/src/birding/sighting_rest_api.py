from http import HTTPStatus
from typing import List

from flask import Blueprint, Response, make_response, jsonify, request

from .authentication_rest_api import require_authentication
from .v0.bird import BirdRepository, Bird
from .sighting import SightingRepository, Sighting
from .time import parse_date
from .time import parse_time
from .account import AccountRepository, Account
from .authentication import JwtDecoder


def create_sighting_rest_api_blueprint(
      token_decoder: JwtDecoder,
      account_repository: AccountRepository,
      sighting_repository: SightingRepository,
      bird_repository: BirdRepository) -> Blueprint:
  blueprint = Blueprint('sighting', __name__)

  @blueprint.route('/profile/<string:username>/sighting')
  @require_authentication(token_decoder, account_repository)
  def get_profile_sightings(username: str, account: Account) -> Response:
    account = account_repository.find_account(username)
    if not account:
      return make_response('', HTTPStatus.NOT_FOUND)
    (sightings, total_rows) = sighting_repository.sightings(
      birder_id=account.birder_id)
    return sightings_response(sightings, False)

  @blueprint.route('/sighting')
  @require_authentication(token_decoder, account_repository)
  def get_sightings(account: Account):
    limit = request.args.get('limit', type=int)
    if limit is not None and limit <= 0:
      return sightings_failure_response('limit-invalid')
    (sightings, total_rows) = sighting_repository.sightings(limit=limit)
    has_more = total_rows > limit if limit is not None else False
    return sightings_response(sightings, has_more)

  @blueprint.route('/sighting/<int:sighting_id>')
  @require_authentication(token_decoder, account_repository)
  def get_sighting(sighting_id: int, account: Account) -> Response:
    sighting = sighting_repository.find_sighting(sighting_id)
    if sighting and sighting.birder_id == account.birder_id:
      return make_response(jsonify(convert_sighting(sighting)), HTTPStatus.OK)
    else:
      return get_sighting_failure_response()

  @blueprint.route('/sighting/<int:sighting_id>', methods=['DELETE'])
  @require_authentication(token_decoder, account_repository)
  def delete_sighting(sighting_id: int, account: Account) -> Response:
    sighting = sighting_repository.find_sighting(sighting_id)
    if not sighting:
      return sighting_deleted_response()
    if sighting.birder_id != account.birder_id:
      return sighting_delete_unauthorized_response()
    sighting_repository.delete_sighting(sighting_id)
    return sighting_deleted_response()

  @blueprint.route('/sighting', methods=['POST'])
  @require_authentication(token_decoder, account_repository)
  def post_sighting(account: Account) -> Response:
    birder_id = request.json['birder']['id']
    if account.birder_id != birder_id:
      return post_sighting_unauthorized_response()
    binomial_name = request.json['bird']['binomialName']
    bird = bird_repository.get_bird_by_binomial_name(binomial_name)
    if not bird:
      return make_response('', HTTPStatus.BAD_REQUEST)
    sighting = create_sighting(request.json, bird)
    sighting = sighting_repository.add_sighting(sighting)
    return post_sighting_success_response(sighting.id)

  def create_sighting(post_data: dict, bird: Bird) -> Sighting:
    return Sighting(
      birder_id=post_data['birder']['id'], bird_id=bird.id,
      sighting_date=parse_date(post_data['date']),
      sighting_time=parse_time(post_data['time']) if 'time' in post_data else None)

  def sightings_failure_response(error_message):
    return make_response(jsonify({
      'error': error_message,
    }), HTTPStatus.BAD_REQUEST)

  def get_sighting_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'You are not authorized to get this sighting'
    }), HTTPStatus.UNAUTHORIZED)

  def sighting_deleted_response() -> Response:
    return make_response('', HTTPStatus.NO_CONTENT)

  def sighting_delete_unauthorized_response() -> Response:
    return make_response('', HTTPStatus.UNAUTHORIZED)

  def post_sighting_success_response(sighting_id: int) -> Response:
    response = make_response(jsonify({
      'status': 'success',
    }), HTTPStatus.CREATED)
    response.headers['Location'] = f'/sighting/{sighting_id}'
    response.autocorrect_location_header = False
    return response

  def post_sighting_unauthorized_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
    }), HTTPStatus.UNAUTHORIZED)

  return blueprint


def sightings_response(sightings: List[Sighting], has_more: bool) -> Response:
  return make_response(jsonify({
    'items': list(map(convert_sighting, sightings)),
    'hasMore': has_more,
  }), HTTPStatus.OK)


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
