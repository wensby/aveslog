import logging
import os
import unittest
from datetime import datetime
from datetime import timedelta
from unittest import TestCase
from unittest.mock import Mock

import psycopg2
from flask import Response
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.datastructures import Headers

import aveslog
from aveslog.v0.account import PasswordHasher
from aveslog.v0.authentication import SaltFactory
from aveslog.v0.authentication import AccessToken
from aveslog.v0.authentication import JwtFactory
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.models import Base


def mock_return(value):
  return Mock(return_value=value)


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
    self._app = aveslog.create_app(test_config=test_config)
    self._app.test_client_class = TestClient
    database_connection_details = aveslog.create_database_connection_details()
    self.database_connection = psycopg2.connect(**database_connection_details)
    self.app_context = self._app.test_request_context()
    self.app_context.push()
    self.client = self._app.test_client()
    logging.disable(logging.CRITICAL)

  def get_with_access_token(self, uri: str, *, account_id: int) -> Response:
    token = self.create_access_token(account_id)
    return self.client.get(uri, headers={'accessToken': token.jwt})

  def db_insert_locale(self, locale_id, code):
    cursor = self.database_connection.cursor()
    cursor.execute('INSERT INTO locale (id, code) VALUES (%s, %s);',
      (locale_id, code))
    self.database_connection.commit()

  def db_delete_refresh_token(self, refresh_token_id: int) -> None:
    cursor = self.database_connection.cursor()
    cursor.execute('DELETE FROM refresh_token WHERE id = %s;',
      (refresh_token_id,))
    self.database_connection.commit()

  def db_insert_registration(self, email, token):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO account_registration (id, email, token) '
      'VALUES (%s, %s, %s);', (4, email, token))
    self.database_connection.commit()

  def db_insert_bird(self, bird_id, binomial_name):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO bird (id, binomial_name) '
      'VALUES (%s, %s);', (bird_id, binomial_name))
    self.database_connection.commit()

  def db_insert_picture(self, picture_id, filepath, credit):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO picture (id, filepath, credit) '
      'VALUES (%s, %s, %s);', (picture_id, filepath, credit)
    )
    self.database_connection.commit()

  def db_insert_bird_thumbnail(self, bird_id, picture_id):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO bird_thumbnail (bird_id, picture_id) '
      'VALUES (%s, %s);', (bird_id, picture_id)
    )
    self.database_connection.commit()

  def db_insert_password_reset_token(self, account_id, token):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO password_reset_token (account_id, token) '
      'VALUES (%s, %s);', (account_id, token))
    self.database_connection.commit()

  def db_insert_sighting(self,
        sighting_id, birder_id, bird_id, sighting_date, sighting_time):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO '
      'sighting (id, birder_id, bird_id, sighting_date, sighting_time) '
      'VALUES (%s, %s, %s, %s, %s);',
      (sighting_id, birder_id, bird_id, sighting_date, sighting_time))
    self.database_connection.commit()

  def db_insert_bird_name(self, bird_name_id, bird_id, locale_id, name):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO bird_name (id, bird_id, locale_id, name) '
      'VALUES (%s, %s, %s, %s);',
      (bird_name_id, bird_id, locale_id, name),
    )
    self.database_connection.commit()

  def db_setup_account(self,
        birder_id: int,
        account_id: int,
        username: str,
        password: str,
        email: str,
  ) -> None:
    password_hasher = PasswordHasher(SaltFactory())
    salt, hash = password_hasher.create_salt_hashed_password(password)
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO birder (id, name) VALUES (%s, %s);',
      (birder_id, username)
    )
    cursor.execute(
      'INSERT INTO account (id, username, email, birder_id, locale_id) '
      'VALUES (%s, %s, %s, %s, %s);',
      (account_id, username, email, birder_id, None)
    )
    cursor.execute(
      'INSERT INTO hashed_password (account_id, salt, salted_hash) '
      'VALUES (%s, %s, %s);',
      (account_id, salt, hash)
    )
    self.database_connection.commit()

  def create_access_token(self, account_id: int) -> AccessToken:
    jwt_factory = JwtFactory(self._app.secret_key)
    token_factory = AuthenticationTokenFactory(jwt_factory, datetime.utcnow)
    return token_factory.create_access_token(account_id, timedelta(1))

  def post_refresh_token(self, username: str, password: str) -> Response:
    resource = '/authentication/refresh-token'
    query = f'username={username}&password={password}'
    return self.client.post(f'{resource}?{query}')

  def tearDown(self) -> None:
    cursor = self.database_connection.cursor()
    cursor.execute('DELETE FROM refresh_token;')
    cursor.execute('DELETE FROM password_reset_token;')
    cursor.execute('DELETE FROM hashed_password;')
    cursor.execute('DELETE FROM account;')
    cursor.execute('DELETE FROM sighting;')
    cursor.execute('DELETE FROM bird_thumbnail;')
    cursor.execute('DELETE FROM picture;')
    cursor.execute('DELETE FROM bird_name;')
    cursor.execute('DELETE FROM bird;')
    cursor.execute('DELETE FROM birder;')
    cursor.execute('DELETE FROM account_registration;')
    cursor.execute('DELETE FROM locale;')
    self.database_connection.commit()
    self.database_connection.close()
    self.app_context.pop()
    logging.disable(logging.NOTSET)

  def db_get_sighting_rows(self):
    cursor = self.database_connection.cursor()
    cursor.execute('SELECT * FROM sighting;')
    self.database_connection.commit()
    return cursor.fetchall()

def create_in_memory_sqlite_database_session(base):
  engine = create_engine('sqlite://')
  base.metadata.create_all(engine)
  return sessionmaker(bind=engine)()