from http import HTTPStatus

from test_util import AppTestCase


class TestBird(AppTestCase):

  def test_get_existing_bird(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', 'myCredit')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'binomialName': 'Pica pica',
        'coverUrl': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
        'thumbnailCredit': 'myCredit',
        'thumbnailUrl': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
      }
    })

  def test_get_bird_by_id(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', 'myCredit')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/birds/1')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'binomialName': 'Pica pica',
        'coverUrl': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
        'thumbnailCredit': 'myCredit',
        'thumbnailUrl': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
      }
    })