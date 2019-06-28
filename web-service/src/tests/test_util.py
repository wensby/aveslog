from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from flask import url_for
from flask.testing import FlaskClient
from requests_html import HTML
from werkzeug.datastructures import Headers

import birding


def mock_return(value):
  return Mock(return_value=value)


class TestClient(FlaskClient):

  def open(self, *args, **kwargs):
    headers = kwargs.pop('headers', Headers())
    kwargs['headers'] = headers
    return super().open(*args, **kwargs)


class AppTestCase(TestCase):

  def setUp(self) -> None:
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    self.app = birding.create_app(test_config=test_config)
    self.database = self.app.db
    self.app.test_client_class = TestClient
    self.app_context = self.app.test_request_context()
    self.app_context.push()
    self.client = self.app.test_client()

  def populate_session(self, key, value):
    with self.client.session_transaction() as session:
      session[key] = value

  def db_insert_account(self, account_id):
    self.app.db.query(
      'INSERT INTO user_account '
      '(id, username, email, person_id, locale_id) '
      'VALUES '
      '(%s, %s, %s, %s, %s);',
      (account_id, 'myUsername', 'myEmail', None, None))

  def get_flashed_messages(self, category):
    with self.client.session_transaction() as session:
      flash_message = dict(session['_flashes']).get(category)
    return flash_message

  def assertRedirect(self, response, endpoint):
    self.assertEqual(response.status_code, HTTPStatus.FOUND)
    html = HTML(html=response.data)
    self.assertListEqual(list(html.links), [url_for(endpoint)])

  def tearDown(self) -> None:
    self.database.query('DELETE FROM user_account;')
    self.database.query('DELETE FROM user_account_registration;')
    self.app_context.pop()
