from http import HTTPStatus
from typing import Union, Optional

from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.account import AccountRepository
from aveslog.v0 import ErrorCode, AccountRegistrationController
from aveslog.v0.models import AccountRegistration
from aveslog.v0.rest_api import RestApiResponse, error_response


class RegistrationRestApi:

  def __init__(self,
        registration_controller: AccountRegistrationController,
        account_repository: AccountRepository,
        locale_repository: LocaleRepository,
        locale_loader: LocaleLoader,
  ):
    self._registration_controller = registration_controller
    self._account_repository = account_repository
    self._locale_repository = locale_repository
    self._locale_loader = locale_loader

  def create_registration_request(self, email: str) -> RestApiResponse:
    result = self._initiate_registration(email)
    if result == 'email taken':
      return error_response(ErrorCode.EMAIL_TAKEN, 'Email taken')
    elif result == 'email invalid':
      return error_response(ErrorCode.EMAIL_INVALID, 'Email invalid')
    return RestApiResponse(HTTPStatus.OK, {})

  def get_registration_request(self, token: str) -> RestApiResponse:
    registration = self._find_registration_token(token)
    if registration:
      return RestApiResponse(HTTPStatus.OK, {
        'email': registration.email,
      })
    return RestApiResponse(HTTPStatus.NOT_FOUND, {})

  def _initiate_registration(self,
        email: str
  ) -> Union[AccountRegistration, str]:
    locale = self._load_english_locale()
    return self._registration_controller.initiate_registration(email, locale)

  def _find_registration_token(self,
        registration_token: str) -> Optional[AccountRegistration]:
    return self._account_repository.find_account_registration_by_token(
      registration_token)

  def _load_english_locale(self) -> LoadedLocale:
    locale = self._locale_repository.find_locale_by_code('en')
    return self._locale_loader.load_locale(locale)
