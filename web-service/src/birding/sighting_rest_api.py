from http import HTTPStatus
from typing import Optional, List

from flask import Blueprint, Response, make_response, jsonify, request

from .account import AccountRepository, Account
from .authentication import AuthenticationTokenDecoder
from .sighting_view import SightingViewFactory, SightingItem


def create_sighting_rest_api_blueprint(
      token_decoder: AuthenticationTokenDecoder,
      account_repository: AccountRepository,
      sighting_view_factory: SightingViewFactory,
) -> Blueprint:
  blueprint = Blueprint('v2sighting', __name__, url_prefix='/v2')

  @blueprint.route('/profile/<string:username>/sighting')
  def get_profile_sightings(username: str) -> Response:
    account = get_authorized_account(request.headers.get('authToken'))
    if account and account.username == username:
      sightings = get_sightings(account)
      return sightings_response(sightings)
    else:
      return failure_response()

  def get_authorized_account(token: Optional[str]) -> Optional[Account]:
    if not token:
      return None
    decode_result = token_decoder.decode_authentication_token(token)
    if decode_result.error:
      return None
    account_id = decode_result.payload['sub']
    return account_repository.find_account_by_id(account_id)

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
    return list(map(lambda item: convert_sighting_item(item, account.person_id),
                    sighting_view_factory.create_sighting_items(account)))

  def sightings_response(sightings: List[dict]) -> Response:
    return make_response(jsonify({
      'status': 'success',
      'result': {
        'sightings': sightings,
      },
    }), HTTPStatus.OK)

  def failure_response() -> Response:
    return make_response(jsonify({
      'status': 'failure',
      'message': 'You are not authorized to get these sightings'
    }), HTTPStatus.UNAUTHORIZED)

  return blueprint
