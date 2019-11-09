from http import HTTPStatus
from flask import Blueprint, make_response, jsonify

from .sighting_rest_api import sightings_response
from .sighting import SightingRepository
from .birder import BirderRepository
from .v0.models import Birder, Account
from .account import AccountRepository
from .authentication import JwtDecoder
from .authentication_rest_api import require_authentication


def create_birder_rest_api_blueprint(
      jwt_decoder: JwtDecoder,
      account_repository: AccountRepository,
      birder_repository: BirderRepository,
      sighting_repository: SightingRepository,
) -> Blueprint:
  blueprint = Blueprint('birders', __name__)

  @blueprint.route('/birders/<int:birder_id>')
  @require_authentication(jwt_decoder, account_repository)
  def get_birder(birder_id: int, account: Account):
    birder = birder_repository.birder_by_id(birder_id)
    if not birder:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response(jsonify(convert_birder(birder)), HTTPStatus.OK)

  @blueprint.route('/birders/<int:birder_id>/sightings')
  @require_authentication(jwt_decoder, account_repository)
  def get_birder_sightings(birder_id: int, account: Account):
    (sightings, total_rows) = sighting_repository.sightings(
      birder_id=birder_id)
    return sightings_response(sightings, False)

  return blueprint


def convert_birder(birder: Birder) -> dict:
  return {
    'id': birder.id,
    'name': birder.name,
  }
