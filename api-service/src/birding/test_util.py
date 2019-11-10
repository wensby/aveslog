import logging
import os
import unittest
from datetime import datetime
from datetime import timedelta
from unittest import TestCase
from unittest.mock import Mock

from flask import Response
from flask.testing import FlaskClient
from psycopg2.pool import SimpleConnectionPool
from werkzeug.datastructures import Headers

import birding
from v0.account import PasswordHasher, Password
from v0.authentication import SaltFactory
from v0.authentication import AccessToken
from v0.authentication import JwtFactory
from v0.authentication import AuthenticationTokenFactory
from v0.database import Transaction
from v0.database import Database


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


class IntegrationTestCase(TestCase):

  @classmethod
  def setUpClass(cls) -> None:
    if 'DATABASE_HOST' not in os.environ:
      raise unittest.SkipTest(
        'Skipping database depending test case ' + str(cls.__name__))


class AppTestCase(IntegrationTestCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.test_rate_limit_per_minute = 60

  def setUp(self) -> None:
    self.maxDiff = None
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002',
      'RATE_LIMIT': f'{self.test_rate_limit_per_minute}/minute',
    }
    self._app = birding.create_app(test_config=test_config)
    self._app.test_client_class = TestClient
    database_connection_details = birding.create_database_connection_details()
    self.pool = SimpleConnectionPool(1, 20, **database_connection_details)
    self._app.db = Database(self._app.logger, self.pool)
    self.database: Database = self._app.db
    self.app_context = self._app.test_request_context()
    self.app_context.push()
    self.client = self._app.test_client()
    logging.disable(logging.CRITICAL)

  def get_with_access_token(self, uri: str, *, account_id: int) -> Response:
    token = self.create_access_token(account_id)
    return self.client.get(uri, headers={'accessToken': token.jwt})

  def db_insert_birder(self, birder_id, name):
    self.database.query(
      'INSERT INTO birder (id, name) VALUES (%s, %s);', (birder_id, name))

  def db_insert_locale(self, locale_id, code):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO locale (id, code) VALUES (%s, %s);', (locale_id, code))

  def db_insert_account(self,
        account_id: int,
        username: str,
        email: str,
        birder_id: int,
        locale_id: int,
  ) -> None:
    self.database.query(
      'INSERT INTO account '
      '(id, username, email, birder_id, locale_id) '
      'VALUES '
      '(%s, %s, %s, %s, %s);',
      (account_id, username, email, birder_id, locale_id))

  def db_delete_refresh_token(self, refresh_token_id: int) -> None:
    with self.database.transaction() as transaction:
      transaction.execute(
        'DELETE FROM refresh_token WHERE id = %s;', (refresh_token_id,))

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
        sighting_id, birder_id, bird_id, sighting_date, sighting_time):
    with self.database.transaction() as transaction:
      transaction.execute(
        'INSERT INTO '
        'sighting (id, birder_id, bird_id, sighting_date, sighting_time) '
        'VALUES (%s, %s, %s, %s, %s);',
        (sighting_id, birder_id, bird_id, sighting_date, sighting_time))

  def db_setup_account(self,
        birder_id: int,
        account_id: int,
        username: str,
        password: str,
        email: str) -> None:
    self.db_insert_birder(birder_id, username)
    self.db_insert_account(account_id, username, email, birder_id, None)
    self.db_insert_password(account_id, password)

  def create_access_token(self, account_id: int) -> AccessToken:
    jwt_factory = JwtFactory(self._app.secret_key)
    token_factory = AuthenticationTokenFactory(jwt_factory, datetime.utcnow)
    return token_factory.create_access_token(account_id, timedelta(1))

  def post_refresh_token(self, username: str, password: str) -> Response:
    resource = '/authentication/refresh-token'
    query = f'username={username}&password={password}'
    return self.client.post(f'{resource}?{query}')

  def tearDown(self) -> None:
    with self.database.transaction() as transaction:
      transaction.execute('DELETE FROM refresh_token;')
      transaction.execute('DELETE FROM password_reset_token;')
      transaction.execute('DELETE FROM hashed_password;')
      transaction.execute('DELETE FROM account;')
      transaction.execute('DELETE FROM sighting;')
      transaction.execute('DELETE FROM bird_thumbnail;')
      transaction.execute('DELETE FROM picture;')
      transaction.execute('DELETE FROM bird;')
      transaction.execute('DELETE FROM birder;')
      transaction.execute('DELETE FROM account_registration;')
      transaction.execute('DELETE FROM locale;')
    self.app_context.pop()
    self.pool.closeall()
    logging.disable(logging.NOTSET)

  def db_get_sighting_rows(self):
    with self.database.transaction() as transaction:
      result = transaction.execute('SELECT * FROM sighting;')
      return result.rows
