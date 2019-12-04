from http import HTTPStatus
from typing import Optional, Union

from flask import current_app, g, request, Response, make_response, jsonify

from aveslog.v0.rest_api import error_response
from aveslog.v0.error import ErrorCode
from aveslog.v0.link import LinkFactory
from aveslog.v0.account import AccountRepository
from aveslog.v0.account import TokenFactory
from aveslog.v0.account import PasswordHasher
from aveslog.v0.authentication import AccountRegistrationController
from aveslog.v0.authentication import SaltFactory
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.models import AccountRegistration


def find_registration_token(registration_token: str) -> Optional[
  AccountRegistration]:
  return g.database_session.query(AccountRegistration). \
    filter(AccountRegistration.token.like(registration_token)).first()


def load_english_locale() -> LoadedLocale:
  locales_directory_path = current_app.config['LOCALES_PATH']
  loader = LocaleLoader(locales_directory_path, {})
  locale_repository = LocaleRepository(locales_directory_path, loader)
  locale = locale_repository.find_locale_by_code('en')
  return loader.load_locale(locale)


def initiate_registration(email: str) -> Union[AccountRegistration, str]:
  locale = load_english_locale()
  link_factory = LinkFactory(
    current_app.config['EXTERNAL_HOST'],
    current_app.config['FRONTEND_HOST'],
  )
  registration_controller = AccountRegistrationController(
    AccountRepository(PasswordHasher(SaltFactory())), g.mail_dispatcher,
    link_factory, TokenFactory())
  return registration_controller.initiate_registration(email, locale)


def post_registration_request() -> Response:
  email = request.json['email']
  result = initiate_registration(email)
  if result == 'email taken':
    return error_response(ErrorCode.EMAIL_TAKEN, 'Email taken')
  elif result == 'email invalid':
    return error_response(ErrorCode.EMAIL_INVALID, 'Email invalid')
  return make_response('', HTTPStatus.OK)


def get_registration_request(token: str) -> Response:
  registration = find_registration_token(token)
  if registration:
    return make_response(jsonify({
      'email': registration.email,
    }), HTTPStatus.OK)
  return make_response('', HTTPStatus.NOT_FOUND)
