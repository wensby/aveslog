from http import HTTPStatus

from aveslog.v0.models import Account
from aveslog.v0.rest_api import RestApiResponse
from aveslog.v0.account import AccountRepository


def account_response_dict(account: Account):
  return {
    'username': account.username,
    'birderId': account.birder_id
  }


class AccountsRestApi:

  def __init__(self, account_repository: AccountRepository):
    self._account_repository = account_repository

  def get_me(self, account: Account) -> RestApiResponse:
    return RestApiResponse(HTTPStatus.OK, account_response_dict(account))

  def get_accounts(self) -> RestApiResponse:
    accounts = self._account_repository.accounts()
    return RestApiResponse(HTTPStatus.OK, {
      'items': list(map(account_response_dict, accounts))
    })
