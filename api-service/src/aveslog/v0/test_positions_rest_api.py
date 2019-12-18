from aveslog.test_util import AppTestCase


class TestGetPosition(AppTestCase):

  def test_get_position(self):
    response = self.client.get('/birds/pica-pica')
