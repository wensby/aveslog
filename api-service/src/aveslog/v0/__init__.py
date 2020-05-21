import os
from http import HTTPStatus

from flask import Blueprint, g, Response

from aveslog.v0.geocoding import Geocoding
from aveslog.v0 import routes
from aveslog.v0.database import EngineFactory
from aveslog.v0.database import SessionFactory
from aveslog.v0.error import ErrorCode
from aveslog.mail import MailDispatcher
from aveslog.v0.localization import Locale
from aveslog.v0.localization import LocaleLoader
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.rest_api import error_response


def create_api_v0_blueprint(mail_dispatcher: MailDispatcher) -> Blueprint:
  blueprint = Blueprint('v0', __name__)

  def register_routes(routes):
    for route in routes:
      rule = route['rule']
      endpoint = route.get('endpoint', None)
      view_func = route['func']
      options = route.get('options', {})
      blueprint.add_url_rule(rule, endpoint, view_func, **options)
      blueprint.add_url_rule(f'/v0{rule}', endpoint, view_func, **options)

  database_connection_details = create_database_connection_details()

  engine_factory = EngineFactory()
  engine = engine_factory.create_engine(**database_connection_details)
  session_factory = SessionFactory(engine)

  register_routes(routes.birds_routes)
  register_routes(routes.search_routes)
  register_routes(routes.locales_routes)
  register_routes(routes.roles_routes)
  register_routes(routes.registration_requests_routes)
  register_routes(routes.sightings_routes)
  register_routes(routes.authentication_routes)
  register_routes(routes.account_routes)
  register_routes(routes.birders_routes)
  register_routes(routes.birder_connections_routes)
  register_routes(routes.bird_look_routes)

  @blueprint.before_request
  def before_request():
    g.mail_dispatcher = mail_dispatcher
    # Setup database session. This is fine even for requests that ultimately
    # didn't require database communication, since the session doesn't actually
    # establish a connection with the database until you start using it.
    g.database_session = session_factory.create_session()

  @blueprint.after_request
  def after_request(response: Response):
    database_session = g.pop('database_session', None)
    if database_session is not None:
      database_session.close()
    return response

  @blueprint.app_errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
  def too_many_requests_handler(e):
    return error_response(
      ErrorCode.RATE_LIMIT_EXCEEDED,
      f'Rate limit exceeded {e.description}',
      status_code=HTTPStatus.TOO_MANY_REQUESTS,
    )

  return blueprint


def create_database_connection_details() -> dict:
  return {
    'host': os.environ.get('DATABASE_HOST'),
    'dbname': os.environ.get('DATABASE_NAME'),
    'user': os.environ.get('DATABASE_USER'),
    'password': os.environ.get('DATABASE_PASSWORD')
  }
