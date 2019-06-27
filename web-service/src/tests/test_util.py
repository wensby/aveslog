from unittest import TestCase
from unittest.mock import Mock
from flask.testing import FlaskClient
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
    self.app.test_client_class = TestClient
