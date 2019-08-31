import json
from http import HTTPStatus

from test_util import AppTestCase


class TestSearch(AppTestCase):

  def test_search_empty_query(self):
    response = self.client.get('/v2/bird?q=')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    self.assertEqual(len(data['result']), 0)

  def test_search_empty_query_when_birds_exist(self):
    self.db_insert_bird(1, 'Pica pica')

    response = self.client.get('/v2/bird?q=')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    self.assertEqual(len(data['result']), 0)

  def test_search_pica_pica_with_thumbnail(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', '')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/v2/bird?q=pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    result = data['result']
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], {
      'birdId': 1,
      'binomialName': 'Pica pica',
      'thumbnail': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg'
    })

  def test_search_pica_pica(self):
    self.db_insert_bird(1, 'Pica pica')

    response = self.client.get('/v2/bird?q=Pica%20pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    result = data['result']
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], { 'birdId': 1, 'binomialName': 'Pica pica' })

  def test_search_by_locale_name(self):
    self.db_insert_locale(1, 'sv')
    self.db_insert_bird(1, 'Pica pica')

    response = self.client.get('/v2/bird?q=Skata')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    result = data['result']
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], { 'birdId': 1, 'binomialName': 'Pica pica' })


class TestBird(AppTestCase):

  def test_get_existing_bird(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', 'myCredit')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/v2/bird/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'binomialName': 'Pica pica',
        'coverUrl': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
        'thumbnailCredit': 'myCredit',
      }
    })

  def test_get_bird_by_id(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', 'myCredit')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/v2/bird/1')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'binomialName': 'Pica pica',
        'coverUrl': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
        'thumbnailCredit': 'myCredit',
      }
    })
