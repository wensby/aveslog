import logging
import os
import unittest
from datetime import datetime
from datetime import timedelta
from unittest import TestCase
from unittest.mock import Mock

from flask import Response

import aveslog
from aveslog.v0 import EngineFactory, SessionFactory
from aveslog.v0.account import PasswordHasher
from aveslog.v0.authentication import SaltFactory
from aveslog.v0.authentication import AccessToken
from aveslog.v0.authentication import JwtFactory
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.app_test_util import test_app_mail_list
from aveslog.app_test_util import test_app
from aveslog.app_test_util import test_app_database_connection
from aveslog.app_test_util import test_app_request_context
from aveslog.app_test_util import test_app_client
from aveslog.app_test_util import test_app_engine


def mock_return(value):
  return Mock(return_value=value)


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
    self.dispatched_mails = test_app_mail_list
    test_app_mail_list.clear()
    self._app = test_app
    self._app.rate_limiter.reset()
    self.database_connection = test_app_database_connection
    self.clear_database()
    self.app_context = test_app_request_context
    self.app_context.push()
    self.client = test_app_client
    self.database_engine = test_app_engine
    logging.disable(logging.CRITICAL)

  def get_with_access_token(self, uri: str, *, account_id: int) -> Response:
    token = self.create_access_token(account_id)
    return self.client.get(uri, headers={'accessToken': token.jwt})

  def db_insert_locale(self, locale_id, code):
    cursor = self.database_connection.cursor()
    cursor.execute('INSERT INTO locale (id, code) VALUES (%s, %s);',
      (locale_id, code))
    self.database_connection.commit()

  def db_insert_role(self, role_id, role_name):
    cursor = self.database_connection.cursor()
    cursor.execute('INSERT INTO role (id, name) VALUES (%s, %s);',
      (role_id, role_name))
    self.database_connection.commit()

  def db_delete_refresh_token(self, refresh_token_id: int) -> None:
    cursor = self.database_connection.cursor()
    cursor.execute('DELETE FROM refresh_token WHERE id = %s;',
      (refresh_token_id,))
    self.database_connection.commit()

  def db_insert_registration(self, email, token):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO registration_request (id, email, token) '
      'VALUES (%s, %s, %s);', (4, email, token))
    self.database_connection.commit()

  def db_insert_position(self, position_id, point):
    coordinates = "POINT(%s %s)" % (point[1], point[0])
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO position (id, point) '
      'VALUES (%s, ST_GeomFromText(%s));', (position_id, coordinates))
    self.database_connection.commit()

  def db_insert_position_name(
        self,
        position_name_id,
        position_id,
        locale_id,
        detail_level,
        name,
        creation_time,
  ):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO position_name (id, position_id, locale_id, detail_level, name, creation_time) '
      'VALUES (%s, %s, %s, %s, %s, %s);',
      (position_name_id, position_id, locale_id, detail_level, name, creation_time))
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

  def db_insert_resource_permission(self, id, resource_regex, method):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO resource_permission (id, resource_regex, method) '
      'VALUES (%s, %s, %s);', (id, resource_regex, method))
    self.database_connection.commit()

  def db_insert_role_resource_permission(self, role_id, resource_permission_id):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO role_resource_permission (role_id, resource_permission_id) '
      'VALUES (%s, %s);', (role_id, resource_permission_id))
    self.database_connection.commit()

  def db_insert_account_role(self, account_id, role_id):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO account_role (account_id, role_id) '
      'VALUES (%s, %s);', (account_id, role_id))
    self.database_connection.commit()

  def db_insert_sighting(
        self,
        sighting_id,
        birder_id,
        bird_id,
        sighting_date,
        sighting_time,
        position_id,
  ):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO '
      'sighting (id, birder_id, bird_id, sighting_date, sighting_time, position_id) '
      'VALUES (%s, %s, %s, %s, %s, %s);',
      (sighting_id, birder_id, bird_id, sighting_date, sighting_time, position_id))
    self.database_connection.commit()

  def db_insert_bird_common_name(self, bird_common_name_id, bird_id, locale_id, name):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO bird_common_name (id, bird_id, locale_id, name) '
      'VALUES (%s, %s, %s, %s);',
      (bird_common_name_id, bird_id, locale_id, name),
    )
    self.database_connection.commit()

  def db_insert_birder(self, birder_id, username):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO birder (id, name) VALUES (%s, %s);', (birder_id, username)
    )
    self.database_connection.commit()

  def db_insert_birder_connection(self, birder_connection_id, primary_birder_id, secondary_birder_id):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'INSERT INTO birder_connection (id, primary_birder_id, secondary_birder_id) '
      'VALUES (%s, %s, %s);', (birder_connection_id, primary_birder_id, secondary_birder_id)
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
    self.clear_database()
    self.app_context.pop()
    logging.disable(logging.NOTSET)

  def clear_database(self):
    cursor = self.database_connection.cursor()
    cursor.execute(
      'DELETE FROM birder_connection;'
      'ALTER SEQUENCE birder_connection_id_seq RESTART WITH 1;'
      'DELETE FROM position_name;'
      'DELETE FROM refresh_token;'
      'DELETE FROM password_reset_token;'
      'DELETE FROM hashed_password;'
      'DELETE FROM account_role;'
      'DELETE FROM role_resource_permission;'
      'DELETE FROM role;'
      'DELETE FROM resource_permission;'
      'DELETE FROM account;'
      'DELETE FROM sighting;'
      'DELETE FROM position;'
      'DELETE FROM bird_thumbnail;'
      'DELETE FROM picture;'
      'DELETE FROM bird_common_name;'
      'DELETE FROM bird_look;'
      'ALTER SEQUENCE bird_look_id_seq RESTART WITH 1;'
      'DELETE FROM bird;'
      'ALTER SEQUENCE bird_id_seq RESTART WITH 1;'
      'DELETE FROM birder;'
      'DELETE FROM registration_request;'
      'DELETE FROM locale;'
      'ALTER SEQUENCE bird_common_name_id_seq RESTART WITH 1;'
    )
    self.database_connection.commit()

  def db_get_sighting_rows(self):
    cursor = self.database_connection.cursor()
    cursor.execute('SELECT * FROM sighting;')
    self.database_connection.commit()
    return cursor.fetchall()

  def db_get_registration_requests(self):
    cursor = self.database_connection.cursor()
    cursor.execute('SELECT * FROM registration_request;')
    self.database_connection.commit()
    return cursor.fetchall()

  def db_get_birder_connections(self):
    cursor = self.database_connection.cursor()
    cursor.execute('SELECT * FROM birder_connection;')
    self.database_connection.commit()
    return cursor.fetchall()


def get_test_database_session():
  engine_factory = EngineFactory(echo=False)
  database_connection_details = aveslog.v0.create_database_connection_details()
  engine = engine_factory.create_engine(**database_connection_details)
  session_factory = SessionFactory(engine)
  return session_factory.create_session()
