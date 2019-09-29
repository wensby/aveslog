from http import HTTPStatus

from flask import Blueprint, make_response, request, jsonify

from birding.authentication_rest_api import create_unauthorized_response
from birding import AccountRepository
from .authentication import AuthenticationTokenDecoder


def create_account_rest_api_blueprint(
      token_decoder: AuthenticationTokenDecoder,
      account_repository: AccountRepository
) -> Blueprint:
  blueprint = Blueprint('account', __name__, url_prefix='/account')

  @blueprint.route('/me')
  def get_me():
    auth_token = request.headers.get('authToken')
    if auth_token:
      decode_result = token_decoder.decode_authentication_token(auth_token)
      if decode_result.ok:
        account = account_repository.find_account_by_id(decode_result.payload['sub'])
        return make_response(jsonify({'status': 'success', 'account': {'username': account.username, 'personId': account.person_id}}), HTTPStatus.OK)
      elif decode_result.error == 'token-invalid':
        return create_unauthorized_response('Authentication token invalid')
      elif decode_result.error == 'signature-expired':
        return create_unauthorized_response('Authentication token expired')
    return create_unauthorized_response('Authentication token missing')

  return blueprint
