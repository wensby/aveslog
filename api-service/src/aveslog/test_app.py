import logging
import os
import shutil
from http import HTTPStatus

import aveslog
from aveslog.app_test_util import TestClient
from aveslog.test_util import IntegrationTestCase


class TestAppCreation(IntegrationTestCase):

  @classmethod
  def setUpClass(cls) -> None:
    super().setUpClass()

  def test_creation(self):
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002'
    }
    aveslog.create_app(test_config=test_config)

  def test_creation_sets_frontend_host_from_environment_variable(self) -> None:
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
    }
    os.environ['FRONTEND_HOST'] = 'http://localhost:3002'

    app = aveslog.create_app(test_config=test_config)

    self.assertEqual(app.config['FRONTEND_HOST'], 'http://localhost:3002')

  def test_creation_crashes_without_frontend_host(self):
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
    }
    self.assertRaises(Exception, aveslog.create_app, test_config=test_config)

  def test_creation_creates_instance_directory(self):
    shutil.rmtree('instance')
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002'
    }
    aveslog.create_app(test_config=test_config)
    self.assertIn('instance', os.listdir('.'))

  def test_creation_fails_if_no_secret_key(self):
    test_config = {
      'TESTING': True,
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002'
    }
    self.assertRaises(Exception, aveslog.create_app, test_config=test_config)

  def test_creation_reads_from_instance_config(self):
    with open('instance/config.py', 'w') as file:
      file.writelines([
        "SECRET_KEY = 'wowsosecret'\n",
        "TESTING = True\n",
        "LOGS_DIR_PATH = 'test-logs'\n",
        "FRONTEND_HOST = 'http://localhost:3002'\n"
      ])
    self.assertTrue(os.path.exists('instance/config.py'))
    aveslog.create_app()

  def test_creation_creates_logs_directory(self):
    shutil.rmtree('test-logs')
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002'
    }
    aveslog.create_app(test_config=test_config)
    self.assertIn('test-logs', os.listdir('.'))

  def tearDown(self) -> None:
    if 'FRONTEND_HOST' in os.environ:
      del os.environ['FRONTEND_HOST']


class TestAppBehindProxy(IntegrationTestCase):

  def setUp(self):
    os.environ['BEHIND_PROXY'] = 'true'
    logging.disable(logging.CRITICAL)

  def test_rate_limits_based_on_x_forwarded_for(self):
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs',
      'FRONTEND_HOST': 'http://localhost:3002',
      'RATE_LIMIT': '1/hour',
    }
    app = aveslog.create_app(test_config=test_config)
    app.test_client_class = TestClient
    with app.test_request_context():
      client = app.test_client()
      client_1_headers = {'X-Forwarded-For': '203.0.113.195'}
      client_2_headers = {'X-Forwarded-For': '150.172.238.178'}
      client.get('/birds/poci-poci', headers=client_1_headers)
      response_1 = client.get('/birds/poci-poci', headers=client_1_headers)
      response_2 = client.get('/birds/poci-poci', headers=client_2_headers)
      self.assertEqual(response_1.status_code, HTTPStatus.TOO_MANY_REQUESTS)
      self.assertEqual(response_2.status_code, HTTPStatus.NOT_FOUND)

  def tearDown(self):
    del os.environ['BEHIND_PROXY']
    logging.disable(logging.NOTSET)
