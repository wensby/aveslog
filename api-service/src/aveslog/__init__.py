import logging
import os
from distutils.util import strtobool
from typing import Optional

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from aveslog.mail import MailDispatcherFactory
from aveslog.v0 import create_api_v0_blueprint


def create_app(test_config: Optional[dict] = None) -> Flask:
  app = Flask(__name__, instance_relative_config=True)
  configure_app(app, test_config)

  # Create blueprint dependencies
  mail_dispatcher_factory = MailDispatcherFactory(app)
  mail_dispatcher = mail_dispatcher_factory.create_dispatcher()

  # Create and register blueprints
  api_v0_blueprint = create_api_v0_blueprint(mail_dispatcher)
  app.register_blueprint(api_v0_blueprint)

  app.logger.info('Flask app constructed')
  return app


def configure_app(app: Flask, test_config: dict) -> None:
  app.config['LOCALES_PATH'] = os.path.join(app.root_path, 'locales')
  app.config['EXTERNAL_HOST'] = os.environ['EXTERNAL_HOST']
  app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
  app.config['JSON_AS_ASCII'] = False
  app.config['RATELIMIT_HEADER_LIMIT'] = 'X-Rate-Limit-Limit'
  app.config['RATELIMIT_HEADER_REMAINING'] = 'X-Rate-Limit-Remaining'
  app.config['RATELIMIT_HEADER_RESET'] = 'X-Rate-Limit-Reset'
  # setting RATELIMIT_HEADER_RETRY_AFTER to the same as RATELIMIT_HEADER_RESET
  # will effectively write over the value of X-Rate-Limit-Reset when the headers
  # are later added by Flask-Limiter. This is intentional, since we want
  # X-Rate-Limit-Reset to contain the time left until the next retry (in
  # seconds), but don't want a RetryAfter header in the response.
  app.config['RATELIMIT_HEADER_RETRY_AFTER'] = 'X-Rate-Limit-Reset'
  if not os.path.isdir(app.instance_path):
    os.makedirs(app.instance_path)
  if test_config:
    app.config.from_mapping(test_config)
  else:
    app.config.from_pyfile('config.py', silent=True)
  if not app.config['SECRET_KEY']:
    raise Exception('Flask secret key not set')
  if not os.path.isdir(app.config['LOGS_DIR_PATH']):
    os.makedirs(app.config['LOGS_DIR_PATH'])
  if 'FRONTEND_HOST' not in app.config and 'FRONTEND_HOST' in os.environ:
    app.config['FRONTEND_HOST'] = os.environ['FRONTEND_HOST']
  elif 'FRONTEND_HOST' not in app.config:
    raise Exception('FRONTEND_HOST not set in environment variables or config.')
  configure_cross_origin_resource_sharing(app)
  if is_behind_proxy():
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
  configure_rate_limiter(app)


def configure_cross_origin_resource_sharing(app: Flask) -> None:
  logging.getLogger('flask_cors').level = logging.DEBUG
  CORS(app, resources={
    r'/*': {
      'supports_credentials': True,
      'expose_headers': 'Location',
      'origins': app.config['FRONTEND_HOST'],
      'max_age': 600,
    }
  })


def is_behind_proxy():
  if not 'BEHIND_PROXY' in os.environ:
    return False
  return bool(strtobool(os.environ['BEHIND_PROXY']))


def configure_rate_limiter(app):
  Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[app.config.get('RATE_LIMIT', '100/second,1000/minute')],
    headers_enabled=True,
  )

  @app.after_request
  def clean_header(response):
    del response.headers['X-RateLimit-Reset']
    return response
