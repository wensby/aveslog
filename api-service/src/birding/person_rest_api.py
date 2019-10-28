from http import HTTPStatus
from flask import Blueprint, make_response, jsonify

from .person import PersonRepository
from .account import AccountRepository, Account
from .authentication import JwtDecoder
from .authentication_rest_api import require_authentication


def create_person_rest_api_blueprint(
      jwt_decoder: JwtDecoder,
      account_repository: AccountRepository,
      person_repository: PersonRepository,
) -> Blueprint:
  blueprint = Blueprint('person', __name__)

  @blueprint.route('/person/<int:person_id>')
  @require_authentication(jwt_decoder, account_repository)
  def get_person(person_id: int, account: Account):
    person = person_repository.person_by_id(person_id)
    if not person:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response(jsonify({
      'personId': person.id,
      'name': person.name,
    }), HTTPStatus.OK)

  return blueprint
