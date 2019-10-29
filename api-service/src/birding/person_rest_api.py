from http import HTTPStatus
from flask import Blueprint, make_response, jsonify

from .sighting_rest_api import sightings_response
from .sighting import SightingRepository
from .person import PersonRepository
from .person import Person
from .account import AccountRepository, Account
from .authentication import JwtDecoder
from .authentication_rest_api import require_authentication


def create_person_rest_api_blueprint(
      jwt_decoder: JwtDecoder,
      account_repository: AccountRepository,
      person_repository: PersonRepository,
      sighting_repository: SightingRepository,
) -> Blueprint:
  blueprint = Blueprint('person', __name__)

  @blueprint.route('/person/<int:person_id>')
  @require_authentication(jwt_decoder, account_repository)
  def get_person(person_id: int, account: Account):
    person = person_repository.person_by_id(person_id)
    if not person:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response(jsonify(convert_person(person)), HTTPStatus.OK)

  @blueprint.route('/birders/<int:birder_id>/sightings')
  @require_authentication(jwt_decoder, account_repository)
  def get_birder_sightings(birder_id: int, account: Account):
    (sightings, total_rows) = sighting_repository.sightings(
      person_id=account.person_id)
    return sightings_response(sightings, False)

  return blueprint


def convert_person(person: Person) -> dict:
  return {
    'id': person.id,
    'name': person.name,
  }
