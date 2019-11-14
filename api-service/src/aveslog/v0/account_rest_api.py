from http import HTTPStatus
from typing import Optional

from aveslog.v0.error import ErrorCode
from aveslog.v0.authentication import AccountRegistrationController
from aveslog.v0.models import Account, AccountRegistration
from aveslog.v0.rest_api import RestApiResponse, error_response
from aveslog.v0.account import AccountRepository


def account_response_dict(account: Account):
  return {
    'username': account.username,
    'birderId': account.birder_id
  }


class AccountsRestApi:

  def __init__(self,
        account_repository: AccountRepository,
        registration_controller: AccountRegistrationController,
  ):
    self._account_repository = account_repository
    self._registration_controller = registration_controller

  def create_account(self, post_json: dict) -> RestApiResponse:
    token = post_json.get('token')
    username = post_json.get('username')
    password = post_json.get('password')
    response = self._try_perform_registration(token, username, password)
    if response == 'success':
      account = self._account_repository.find_account(username)
      return RestApiResponse(HTTPStatus.CREATED, {
        'id': account.id,
        'username': account.username,
        'email': account.email,
        'birder': {
          'id': account.birder.id,
          'name': account.birder.name,
        },
      })
    elif response == 'username taken':
      return error_response(
        ErrorCode.USERNAME_TAKEN,
        'Username taken',
        HTTPStatus.CONFLICT,
      )

  def get_me(self, account: Account) -> RestApiResponse:
    return RestApiResponse(HTTPStatus.OK, account_response_dict(account))

  def get_accounts(self) -> RestApiResponse:
    accounts = self._account_repository.accounts()
    return RestApiResponse(HTTPStatus.OK, {
      'items': list(map(account_response_dict, accounts))
    })

  def _try_perform_registration(self,
        registration_token: str,
        username: str,
        password: str,
  ) -> str:
    registration = self._find_registration_token(registration_token)
    return self._registration_controller.perform_registration(
      registration.email, registration.token, username, password)

  def _find_registration_token(self,
        registration_token: str) -> Optional[AccountRegistration]:
    return self._account_repository.find_account_registration_by_token(
      registration_token)
