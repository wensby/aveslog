import os
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import Mock

from flask import url_for
from flask.testing import FlaskClient
from requests_html import HTML
from werkzeug.datastructures import Headers

import birding
from birding.account import PasswordHasher, Password, Account
from birding.authentication import SaltFactory
from birding.database import Transaction
from birding.database import Database


def mock_return(value):
  return Mock(return_value=value)


def mock_database_transaction():
  transaction = Mock(spec=Transaction)
  transaction.__enter__ = Mock(return_value=transaction)
  transaction.__exit__ = Mock(return_value=None)
  return transaction


class TestClient(FlaskClient):

  def open(self, *args, **kwargs):
    headers = kwargs.pop('headers', Headers())
    kwargs['headers'] = headers
    return super().open(*args, **kwargs)


class AppTestCase(TestCase):

  @classmethod
  def setUpClass(cls):
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002'
    }
    cls._app = birding.create_app(test_config=test_config)
    cls._app.test_client_class = TestClient

  def setUp(self) -> None:
    self.database: Database = self._app.db
    self.app_context = self._app.test_request_context()
    self.app_context.push()
    self.client = self._app.test_client()

  def assertFileExist(self, path):
    self.assertTrue(os.path.exists(path))

  def populate_session(self, key, value):
    with self.client.session_transaction() as session:
      session[key] = value

  def assertSessionContains(self, key, value):
    with self.client.session_transaction() as session:
      self.assertIn(key, session)
      self.assertEqual(session[key], value)

  def db_insert_person(self, person_id):
    self.database.query(
      'INSERT INTO person (id, name) VALUES (%s, %s);', (person_id, 'name'))

  def db_insert_locale(self, locale_id, code):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO locale (id, code) VALUES (%s, %s);', (locale_id, code))

  def db_insert_account(self, account_id, username, email, person_id,
        locale_id):
    self.database.query(
      'INSERT INTO account '
      '(id, username, email, person_id, locale_id) '
      'VALUES '
      '(%s, %s, %s, %s, %s);',
      (account_id, username, email, person_id, locale_id))

  def db_delete_account(self, account_id):
    with self.database.transaction() as transaction:
      transaction.execute(
        'DELETE FROM account WHERE id = %s;', (account_id,))

  def db_insert_password(self, account_id, password):
    password_hasher = PasswordHasher(SaltFactory())
    p = Password(password)
    salt_hashed_password = password_hasher.create_salt_hashed_password(p)
    salt = salt_hashed_password[0]
    hashed_password = salt_hashed_password[1]
    self.database.query(
      'INSERT INTO hashed_password (account_id, salt, salted_hash) '
      'VALUES (%s, %s, %s);', (account_id, salt, hashed_password))

  def db_insert_registration(self, email, token):
    self.database.query(
      'INSERT INTO account_registration (id, email, token) '
      'VALUES (%s, %s, %s);', (4, email, token))

  def db_insert_bird(self, bird_id, binomial_name):
    self.database.query(
      'INSERT INTO bird (id, binomial_name) '
      'VALUES (%s, %s);', (bird_id, binomial_name))

  def db_insert_picture(self, picture_id, filepath, credit):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO picture (id, filepath, credit) '
        'VALUES (%s, %s, %s);', (picture_id, filepath, credit)
      )

  def db_insert_bird_thumbnail(self, bird_id, picture_id):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO bird_thumbnail (bird_id, picture_id) '
        'VALUES (%s, %s);', (bird_id, picture_id)
      )

  def db_insert_password_reset_token(self, account_id, token):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO password_reset_token (account_id, token) '
        'VALUES (%s, %s);', (account_id, token))

  def db_insert_sighting(self,
        sighting_id, person_id, bird_id, sighting_date, sighting_time):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO '
        'sighting (id, person_id, bird_id, sighting_date, sighting_time) '
        'VALUES (%s, %s, %s, %s, %s);',
        (sighting_id, person_id, bird_id, sighting_date, sighting_time))

  def db_get_account(self, account_id) -> Account:
    with self.database.transaction() as transaction:
      result = transaction.execute(
        'SELECT * FROM account WHERE id = %s;',
        (account_id,), Account.fromrow)
      return next(iter(result.rows), None)

  def db_setup_account(self,
        person_id: int,
        account_id: int,
        username: str,
        password: str,
        email: str) -> None:
    self.db_insert_person(person_id)
    self.db_insert_account(account_id, username, email, person_id, None)
    self.db_insert_password(account_id, password)

  def get_authentication_token(self, username, password) -> str:
    resource = '/authentication/token'
    query = f'?username={username}&password={password}'
    return self.client.get(f'{resource}{query}').json['accessToken']

  def get_flashed_messages(self, category='message'):
    with self.client.session_transaction() as session:
      if '_flashes' in session:
        return dict(session['_flashes']).get(category)

  def set_logged_in(self, account_id):
    self.populate_session('account_id', account_id)

  def assertRedirect(self, response, endpoint, **values):
    self.assertEqual(response.status_code, HTTPStatus.FOUND)
    html = HTML(html=response.data)
    self.assertListEqual(list(html.links), [url_for(endpoint, **values)])

  def assertOkHtmlResponse(self, response):
    self.assertEqual(response.status_code, HTTPStatus.OK)
    return HTML(html=response.data)

  def assertOkHtmlResponseWithText(self, response, member):
    html = self.assertOkHtmlResponse(response)
    self.assertIn(member, html.full_text)

  def assertOkHtmlResponseWithoutText(self, response, member):
    html = self.assertOkHtmlResponse(response)
    self.assertNotIn(member, html.full_text)

  def assertOkHtmlResponseWith(self, response, xpath):
    html = self.assertOkHtmlResponse(response)
    self.assertTrue(html.xpath(xpath, first=True))

  def tearDown(self) -> None:
    with self.database.transaction() as transaction:
      transaction.execute('DELETE FROM password_reset_token;')
      transaction.execute('DELETE FROM hashed_password;')
      transaction.execute('DELETE FROM account;')
      transaction.execute('DELETE FROM sighting;')
      transaction.execute('DELETE FROM bird_thumbnail;')
      transaction.execute('DELETE FROM picture;')
      transaction.execute('DELETE FROM bird;')
      transaction.execute('DELETE FROM person;')
      transaction.execute('DELETE FROM account_registration;')
      transaction.execute('DELETE FROM locale;')
    self.app_context.pop()

  def assertFlashedMessage(self, category, message):
    self.assertEqual(self.get_flashed_messages(category), message)

  def db_get_password_reset_token_rows(self):
    with self.database.transaction() as transaction:
      result = transaction.execute('SELECT * FROM password_reset_token;')
      rows = result.rows
    return rows

  def db_get_sighting_rows(self):
    with self.database.transaction() as transaction:
      result = transaction.execute('SELECT * FROM sighting;')
      return result.rows
