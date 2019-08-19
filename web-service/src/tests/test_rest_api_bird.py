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
