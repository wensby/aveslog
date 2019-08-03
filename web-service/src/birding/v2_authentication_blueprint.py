from http import HTTPStatus
from flask import Blueprint
from flask import make_response
from flask import jsonify
from flask import request

from .authentication import AuthenticationTokenFactory, Authenticator
from .account import Credentials
from .account import Username
from .account import Password


def create_v2_authentication_blueprint(
      authenticator: Authenticator,
      authentication_token_factory: AuthenticationTokenFactory):
  blueprint = Blueprint('v2authentication', __name__,
                        url_prefix='/v2/authentication')

  @blueprint.route('/login', methods=['POST'])
  def post_login():
    username = request.form['username']
    password = request.form['password']
    if Username.is_valid(username) and Password.is_valid(password):
      credentials = Credentials(Username(username), Password(password))
      account = authenticator.get_authenticated_user_account(credentials)
      if account:
        token = authentication_token_factory.create_authentication_token(
          account.id)
        response = {
          'status': 'success',
          'message': 'Successfully logged in.',
          'auth_token': token
        }
        return make_response(jsonify(response), HTTPStatus.OK)
    response = {
      'status': 'failure',
      'message': 'Try again'
    }
    return make_response(jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR)

  return blueprint
