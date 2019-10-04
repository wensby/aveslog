from http import HTTPStatus

from flask import Blueprint, make_response, jsonify

from .account import Account
from .authentication_rest_api import require_authentication
from birding import AccountRepository
from .authentication import AuthenticationTokenDecoder


def create_account_rest_api_blueprint(
      token_decoder: AuthenticationTokenDecoder,
      account_repository: AccountRepository
) -> Blueprint:
  blueprint = Blueprint('account', __name__, url_prefix='/account')

  @blueprint.route('/me')
  @require_authentication(token_decoder, account_repository)
  def get_me(account: Account):
    return make_response(jsonify({
      'status': 'success',
      'account': account_response_dict(account)
    }), HTTPStatus.OK)

  @blueprint.route('')
  @require_authentication(token_decoder, account_repository)
  def get_accounts(account: Account):
    accounts = account_repository.accounts()
    return make_response(jsonify({
      'status': 'success',
      'result': list(map(account_response_dict, accounts)),
    }))

  def account_response_dict(account):
    return {
      'username': account.username,
      'personId': account.person_id
    }

  return blueprint
