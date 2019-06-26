from unittest import TestCase

import birding


class TestApp(TestCase):

  def test_creation(self):
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    app = birding.create_app(test_config=test_config)