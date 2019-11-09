from http import HTTPStatus

from test_util import AppTestCase


class TestSearchBirds(AppTestCase):

  def test_search_empty_query(self):
    response = self.client.get('/search/birds?q=')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [],
    })

  def test_search_empty_query_when_birds_exist(self):
    self.db_insert_bird(1, 'Pica pica')

    response = self.client.get('/search/birds?q=')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': []
    })

  def test_search_pica_pica_with_thumbnail(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_picture(1, 'image/bird/pica-pica-thumb.jpg', '')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/search/birds?q=pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 'pica-pica',
          'binomialName': 'Pica pica',
          'thumbnail': 'myExternalHost/static/image/bird/pica-pica-thumb.jpg',
          'score': 0.6153846153846154,
        }
      ]
    })

  def test_get_birds_with_custom_page_size(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_bird(2, 'Passer domesticus')

    response = self.client.get('/search/birds?q=P&page_size=1')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 'pica-pica',
          'binomialName': 'Pica pica',
          'score': 0.2
        }
      ]
    })

  def test_search_pica_pica(self):
    self.db_insert_bird(1, 'Pica pica')

    response = self.client.get('/search/birds?q=Pica%20pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 'pica-pica',
          'binomialName': 'Pica pica',
          'score': 1,
        }
      ]
    })

  def test_search_by_locale_name(self):
    self.db_insert_locale(1, 'sv')
    self.db_insert_bird(1, 'Pica pica')

    response = self.client.get('/search/birds?q=Skata')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 'pica-pica',
          'binomialName': 'Pica pica',
          'score': 1,
        }
      ]
    })