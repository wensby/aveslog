from http import HTTPStatus

from test_util import AppTestCase


class TestBird(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')

  def test_get_bird(self):
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', 'myCredit')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'id': 'pica-pica',
      'binomialName': 'Pica pica',
      'thumbnail': {
        'url': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
        'credit': 'myCredit',
      },
      'cover': {
        'url': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
        'credit': 'myCredit',
      },
    })

  def test_get_bird_with_minimal_data(self):
    response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'id': 'pica-pica',
      'binomialName': 'Pica pica',
    })
