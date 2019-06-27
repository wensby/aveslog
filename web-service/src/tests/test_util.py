from unittest.mock import Mock
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers


def mock_return(value):
  return Mock(return_value=value)

class TestClient(FlaskClient):

  def open(self, *args, **kwargs):
    headers = kwargs.pop('headers', Headers())
    kwargs['headers'] = headers
    return super().open(*args, **kwargs)
