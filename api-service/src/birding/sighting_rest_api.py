from http import HTTPStatus
from typing import List

from flask import Blueprint, Response, make_response, jsonify, request

from .authentication_rest_api import require_authentication
from .bird import BirdRepository, Bird
from .sighting import SightingRepository, SightingPost, Sighting
from .time import parse_date
from .time import parse_time
from .account import AccountRepository, Account
from .authentication import AuthenticationTokenDecoder
from .sighting_view import SightingViewFactory, SightingItem


def create_sighting_rest_api_blueprint(
      token_decoder: AuthenticationTokenDecoder,
      account_repository: AccountRepository,
      sighting_view_factory: SightingViewFactory,
      sighting_repository: SightingRepository,
      bird_repository: BirdRepository) -> Blueprint:
  blueprint = Blueprint('sighting', __name__)

  @blueprint.route('/profile/<string:username>/sighting')
  @require_authentication(token_decoder, account_repository)
  def get_profile_sightings(username: str, account: Account) -> Response:
    account = account_repository.find_user_account(username)
    if not account:
      return make_response('', HTTPStatus.NOT_FOUND)
    sightings = get_sightings(account)
    return sightings_response(sightings)

  @blueprint.route('/sighting/<int:sighting_id>')
  @require_authentication(token_decoder, account_repository)
  def get_sighting(sighting_id: int, account: Account) -> Response:
    sighting = sighting_repository.find_sighting(sighting_id)
    if sighting and sighting.person_id == account.person_id:
      return sighting_response(sighting)
    else:
      return get_sighting_failure_response()

  @blueprint.route('/sighting/<int:sighting_id>', methods=['DELETE'])
  @require_authentication(token_decoder, account_repository)
  def delete_sighting(sighting_id: int, account: Account) -> Response:
    sighting = sighting_repository.find_sighting(sighting_id)
    if not sighting:
      return sighting_deleted_response()
    if sighting.person_id != account.person_id:
      return sighting_delete_unauthorized_response()
    sighting_repository.delete_sighting(sighting_id)
    return sighting_deleted_response()

  @blueprint.route('/sighting', methods=['POST'])
  @require_authentication(token_decoder, account_repository)
  def post_sighting(account: Account) -> Response:
    person_id = request.json['person']['id']
    if account.person_id != person_id:
      return post_sighting_unauthorized_response()
    binomial_name = request.json['bird']['binomialName']
    bird = bird_repository.get_bird_by_binomial_name(binomial_name)
    if not bird:
      return make_response('', HTTPStatus.BAD_REQUEST)
    sighting_post = create_sighting_post(request.json, bird)
    sighting = sighting_repository.add_sighting(sighting_post)
    return post_sighting_success_response(sighting.id)

  def convert_sighting(sighting: Sighting) -> dict:
    result = {
      'sightingId': sighting.id,
      'personId': sighting.person_id,
      'birdId': sighting.bird_id,
      'date': sighting.sighting_date.isoformat(),
    }
    if sighting.sighting_time:
      result['time'] = sighting.sighting_time.isoformat()
    return result

  def convert_sighting_item(item: SightingItem, person_id: int) -> dict:
    result = {
      'sightingId': item.sighting_id,
      'personId': person_id,
      'birdId': item.bird_id,
    }
    split_time = item.time.split()
    if len(split_time) > 1:
      result['date'] = split_time[0]
      result['time'] = split_time[1]
    else:
      result['date'] = item.time
    return result

  def get_sightings(account: Account) -> List[dict]:
    items = sighting_view_factory.create_sighting_items(account)
    to_dict = lambda item: convert_sighting_item(item, account.person_id)
    return list(map(to_dict, items))

  def create_sighting_post(post_data: dict, bird: Bird) -> SightingPost:
    person_id = post_data['person']['id']
    date = parse_date(post_data['date'])
    time = parse_time(post_data['time']) if 'time' in post_data else None
    return SightingPost(person_id, bird.id, date, time)

  def sightings_response(sightings: List[dict]) -> Response:
    return make_response(jsonify({
      'status': 'success',
      'result': {
        'sightings': sightings,
      },
    }), HTTPStatus.OK)

  def sighting_response(sighting: Sighting) -> Response:
    return make_response(jsonify({
      'status': 'success',
      'result': convert_sighting(sighting),
    }), HTTPStatus.OK)

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
