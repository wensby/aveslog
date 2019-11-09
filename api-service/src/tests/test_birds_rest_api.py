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
    self.assertDictEqual(response.json, {
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
    self.assert_rate_limit_headers(response)

  def test_get_bird_with_minimal_data(self):
    response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'id': 'pica-pica',
      'binomialName': 'Pica pica',
    })
    self.assert_rate_limit_headers(response)

  def test_get_bird_rate_limited(self):
    response = None

    for _ in range(61):
      response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.TOO_MANY_REQUESTS)
    self.assertDictEqual(response.json, {
      'error': 'rate limit exceeded 60 per 1 minute'
    })
    self.assert_rate_limit_headers(response)

  def assert_rate_limit_headers(self, response):
    self.assertIn('X-Rate-Limit-Limit', response.headers)
    self.assertIn('X-Rate-Limit-Remaining', response.headers)
    self.assertIn('X-Rate-Limit-Reset', response.headers)
    self.assertNotIn('Retry-After', response.headers)
