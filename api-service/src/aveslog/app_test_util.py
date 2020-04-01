import psycopg2
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers

import aveslog
from aveslog.mail import MailDispatcher
from aveslog.v0 import create_database_connection_details


class TestClient(FlaskClient):

  def open(self, *args, **kwargs):
    headers = kwargs.pop('headers', Headers())
    kwargs['headers'] = headers
    return super().open(*args, **kwargs)


class TestMailDispatcher(MailDispatcher):

  def __init__(self, dispatched_mails: list):
    self._dispatched_mails: list = dispatched_mails

  def dispatch(self, recipient, subject, body):
    self._dispatched_mails.append({
      'recipient': recipient,
      'subject': subject,
      'body': body
    })


def create_test_app(mail_list):
  test_config = {
    'TESTING': True,
    'SECRET_KEY': 'wowsosecret',
    'LOGS_DIR_PATH': 'test-logs',
    'FRONTEND_HOST': 'http://localhost:3002',
    'RATE_LIMIT': f'60/minute',
  }

  app = aveslog.create_app_with_dependencies(
    lambda app: TestMailDispatcher(mail_list),
    test_config=test_config,
  )
  app.test_client_class = TestClient
  return app


connection_details = create_database_connection_details()

test_app_mail_list = []
test_app = create_test_app(test_app_mail_list)
test_app_request_context = test_app.test_request_context()
test_app_database_connection = psycopg2.connect(**connection_details)
test_app_client = test_app.test_client()
