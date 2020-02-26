from http import HTTPStatus

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
from aveslog.v0.models import RegistrationRequest


def post_registration_request() -> Response:
  email = request.json['email']
  locale = load_english_locale()
  link_factory = LinkFactory(
    current_app.config['EXTERNAL_HOST'],
    current_app.config['FRONTEND_HOST'],
  )
  account_repository = AccountRepository(PasswordHasher(SaltFactory()))
  token_factory = TokenFactory()
  registration_controller = AccountRegistrationController(
    account_repository,
    g.mail_dispatcher,
    link_factory,
    token_factory)
  result = registration_controller.initiate_registration(email, locale)
  if result == 'email taken':
    return error_response(ErrorCode.EMAIL_TAKEN, 'Email taken')
  elif result == 'email invalid':
    return error_response(ErrorCode.EMAIL_INVALID, 'Email invalid')
  return make_response('', HTTPStatus.CREATED)


def get_registration_request(token: str) -> Response:
  registration_request = g.database_session.query(RegistrationRequest) \
    .filter_by(token=token).first()
  if registration_request:
    return make_response(jsonify({
      'token': registration_request.token,
      'email': registration_request.email,
    }), HTTPStatus.OK)
  return make_response('', HTTPStatus.NOT_FOUND)


def load_english_locale() -> LoadedLocale:
  locales_directory_path = current_app.config['LOCALES_PATH']
  loader = LocaleLoader(locales_directory_path)
  locale_repository = LocaleRepository(locales_directory_path, loader)
  locale = locale_repository.find_locale_by_code('en')
  return loader.load_locale(locale)
