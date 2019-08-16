from http import HTTPStatus
from flask import Blueprint
from flask import make_response
from flask import jsonify
from flask import request

from .localization import LocaleLoader
from .localization import LocaleRepository
from .authentication import AuthenticationTokenFactory, Authenticator
from .authentication import AccountRegistrationController
from .account import Credentials
from .account import Username
from .account import Password


def create_v2_authentication_blueprint(
      authenticator: Authenticator,
      account_registration_controller: AccountRegistrationController,
      locale_repository: LocaleRepository,
      locale_loader: LocaleLoader,
      authentication_token_factory: AuthenticationTokenFactory):
  blueprint = Blueprint('v2authentication', __name__,
                        url_prefix='/v2/authentication')

  @blueprint.route('/token')
  def get_token():
    username = request.args.get('username')
    password = request.args.get('password')
    if Username.is_valid(username) and Password.is_valid(password):
      credentials = Credentials(Username(username), Password(password))
      account = authenticator.get_authenticated_user_account(credentials)
      if account:
        token = authentication_token_factory.create_authentication_token(
          account.id)
        response = {
          'status': 'success',
          'message': 'Successfully logged in.',
          'authToken': token
        }
        return make_response(jsonify(response), HTTPStatus.OK)
    response = {
      'status': 'failure',
      'message': 'Try again'
    }
    return make_response(jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR)

  @blueprint.route('/registration', methods=['POST'])
  def post_registration_email():
    email = request.json['email']
    locale = locale_repository.find_locale_by_code('en')
    loaded_locale = locale_loader.load_locale(locale)
    result = account_registration_controller.initiate_registration(
      email, loaded_locale)
    if result == 'email taken':
      response = {
        'status': 'failure',
        'message': 'Email taken',
      }
      return make_response(jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR)
    elif result == 'email invalid':
      response = {
        'status': 'failure',
        'message': 'Email invalid',
      }
      return make_response(jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
      response = {
        'status': 'success',
      }
      return make_response(jsonify(response), HTTPStatus.OK)

  return blueprint
