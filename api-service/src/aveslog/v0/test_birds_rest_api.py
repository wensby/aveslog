from http import HTTPStatus

from aveslog.test_util import AppTestCase
from aveslog.v0 import ErrorCode


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
    self.assert_rate_limit_headers(response, 59)

  def test_get_bird_with_minimal_data(self):
    response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'id': 'pica-pica',
      'binomialName': 'Pica pica',
    })
    self.assert_rate_limit_headers(response, 59)

  def test_get_bird_rate_limited(self):
    response = None

    for _ in range(61):
      response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.TOO_MANY_REQUESTS)
    self.assertDictEqual(response.json, {
      'code': ErrorCode.RATE_LIMIT_EXCEEDED,
      'message': 'Rate limit exceeded 60 per 1 minute'
    })
    self.assert_rate_limit_headers(response, 0)

  def test_get_bird_when_not_found(self):
    response = self.client.get('/birds/content-not-found')

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    self.assertDictEqual(response.json, {
      'message': 'Not Found'
    })

  def assert_rate_limit_headers(self, response, expected_remaining):
    headers = response.headers
    self.assertIn('X-Rate-Limit-Limit', headers)
    self.assertIn('X-Rate-Limit-Remaining', headers)
    self.assertIn('X-Rate-Limit-Reset', headers)
    self.assertNotIn('Retry-After', headers)
    self.assertNotIn('X-RateLimit-Reset', headers)
    reset = int(headers['X-Rate-Limit-Reset'])
    limit = int(headers['X-Rate-Limit-Limit'])
    remaining = int(headers['X-Rate-Limit-Remaining'])
    self.assertLessEqual(reset, self.test_rate_limit_per_minute)
    self.assertEqual(limit, self.test_rate_limit_per_minute)
    self.assertEqual(remaining, expected_remaining)
