import os
import shutil
from unittest import TestCase

import birding


class TestAppCreation(TestCase):

  def test_creation(self):
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    birding.create_app(test_config=test_config)

  def test_creation_creates_instance_directory(self):
    shutil.rmtree('instance')
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    birding.create_app(test_config=test_config)
    self.assertIn('instance', os.listdir('.'))

  def test_creation_fails_if_no_secret_key(self):
    test_config = {'TESTING': True}
    self.assertRaises(Exception, birding.create_app, test_config=test_config)

  def test_creation_reads_from_instance_config(self):
    with open('instance/config.py', 'w') as file:
      file.writelines(["SECRET_KEY = 'wowsosecret'\n", "TESTING = True\n"])
    self.assertTrue(os.path.exists('instance/config.py'))
    birding.create_app()
