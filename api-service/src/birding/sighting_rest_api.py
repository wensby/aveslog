from http import HTTPStatus
from typing import Optional, List

from flask import Blueprint, Response, make_response, jsonify, request

from .bird import BirdRepository
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
  def get_profile_sightings(username: str) -> Response:
    authenticated_account = get_authorized_account(request.headers.get('authToken'))
    if not authenticated_account:
      return failure_response()
    account = account_repository.find_user_account(username)
    if not account:
      return failure_response()
    sightings = get_sightings(account)
    return sightings_response(sightings)

  @blueprint.route('/sighting/<int:sighting_id>')
  def get_sighting(sighting_id: int) -> Response:
    sighting = sighting_repository.find_sighting(sighting_id)
    account = get_authorized_account(request.headers.get('authToken'))
    if sighting and sighting.person_id == account.person_id:
      return sighting_response(sighting)
    else:
      return get_sighting_failure_response()

  @blueprint.route('/sighting/<int:sighting_id>', methods=['DELETE'])
  def delete_sighting(sighting_id: int) -> Response:
    sighting = sighting_repository.find_sighting(sighting_id)
    if not sighting:
      return sighting_deleted_response()
    account = get_authorized_account(request.headers.get('authToken'))
    if not account or sighting.person_id != account.person_id:
      return sighting_delete_unauthorized_response()
    sighting_repository.delete_sighting(sighting_id)
    return sighting_deleted_response()

  @blueprint.route('/sighting', methods=['POST'])
  def post_sighting() -> Response:
    account = get_authorized_account(request.headers.get('authToken'))
    person_id = request.json['person']['id']
    if account and account.person_id == person_id:
      sighting_post = create_sighting_post(request.json)
      added = sighting_repository.add_sighting(sighting_post)
      if added:
        return post_sighting_success_response()
    else:
      return post_sighting_failure_response()

  def get_authorized_account(token: Optional[str]) -> Optional[Account]:
    if not token:
      return None
    decode_result = token_decoder.decode_authentication_token(token)
    if decode_result.error:
      return None
    account_id = decode_result.payload['sub']
    return account_repository.find_account_by_id(account_id)

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

  def create_sighting_post(post_data: dict) -> SightingPost:
    binomial_name = post_data['bird']['binomialName']
    bird = bird_repository.get_bird_by_binomial_name(binomial_name)
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

  def failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'You are not authorized to get these sightings'
    }), HTTPStatus.UNAUTHORIZED)

  def get_sighting_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'You are not authorized to get this sighting'
    }), HTTPStatus.UNAUTHORIZED)

  def sighting_deleted_response() -> Response:
    return make_response('', HTTPStatus.NO_CONTENT)

  def sighting_delete_unauthorized_response() -> Response:
    return make_response('', HTTPStatus.UNAUTHORIZED)

  def post_sighting_success_response() -> Response:
    return make_response(jsonify({
      'status': 'success',
    }), HTTPStatus.OK)

  def post_sighting_failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
    }), HTTPStatus.UNAUTHORIZED)

  return blueprint
