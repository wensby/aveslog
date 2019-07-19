import os
import shutil
from unittest import TestCase

import birding
from test_util import AppTestCase


class TestAppCreation(TestCase):

  def test_creation(self):
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs'
    }
    birding.create_app(test_config=test_config)

  def test_creation_creates_instance_directory(self):
    shutil.rmtree('instance')
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs'
    }
    birding.create_app(test_config=test_config)
    self.assertIn('instance', os.listdir('.'))

  def test_creation_fails_if_no_secret_key(self):
    test_config = {
      'TESTING': True,
      'LOGS_DIR_PATH': 'test-logs'
    }
    self.assertRaises(Exception, birding.create_app, test_config=test_config)

  def test_creation_reads_from_instance_config(self):
    with open('instance/config.py', 'w') as file:
      file.writelines([
        "SECRET_KEY = 'wowsosecret'\n",
        "TESTING = True\n",
        "LOGS_DIR_PATH = 'test-logs'\n"
      ])
    self.assertTrue(os.path.exists('instance/config.py'))
    birding.create_app()

  def test_creation_creates_logs_directory(self):
    shutil.rmtree('test-logs')
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs'
    }
    birding.create_app(test_config=test_config)
    self.assertIn('test-logs', os.listdir('.'))


class TestGeneralFunctionality(AppTestCase):

  def test_saves_locales_misses_after_request(self):
    self.db_insert_locale(1, 'xx')
    headers = {'Accept-Language': 'xx'}

    self.client.get('/', headers=headers)

    self.assertFileExist('test-logs/locales-misses/xx.txt')