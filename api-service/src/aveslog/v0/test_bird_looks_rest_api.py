from http import HTTPStatus

from aveslog.test_util import AppTestCase


class TestGetBirdLook(AppTestCase):

  def test_get(self):
    self.db_insert_bird(2, 'Pica pica')
    self.db_insert_bird_look(1, 2)
    response = self.client.get('/bird-looks/1')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'id': 1,
      'birdId': 'pica-pica',
      'label': 'label',
      'description': 'description',
    })
