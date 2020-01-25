from datetime import date
from http import HTTPStatus

from aveslog.test_util import AppTestCase
from aveslog.v0 import ErrorCode


class TestBird(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')

  def test_get_bird(self):
    self.db_insert_locale(1, 'sv')
    self.db_insert_locale(2, 'en')
    self.db_insert_locale(3, 'ko')
    self.db_insert_bird_name(1, 1, 1, 'Skata')
    self.db_insert_bird_name(2, 1, 2, 'Eurasian Magpie')
    self.db_insert_bird_name(3, 1, 3, '까치')
    self.db_insert_picture(1, 'myPictureUrl', 'myCredit')
    self.db_insert_bird_thumbnail(1, 1)

    response = self.client.get('/birds/pica-pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.headers['Cache-Control'], 'max-age=300')
    self.assertDictEqual(response.json, {
      'id': 'pica-pica',
      'binomialName': 'Pica pica',
      'commonNames': {
        'sv': ['Skata'],
        'en': ['Eurasian Magpie'],
        'ko': ['까치'],
      },
      'thumbnail': {
        'url': 'myPictureUrl',
        'credit': 'myCredit',
      },
      'cover': {
        'url': 'myPictureUrl',
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


class TestGetBirdStatistics(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')

  def test_get_bird_statistics(self):
    self.db_setup_account(2, 3, 'hulot', 'password', 'hulot@email.com')
    self.db_setup_account(4, 5, 'kenny', 'password', 'kenny@email.com')
    self.db_insert_sighting(6, 2, 1, date(2020, 1, 14), None, None)
    self.db_insert_sighting(7, 2, 1, date(2020, 1, 14), None, None)

    response = self.client.get('/birds/pica-pica/statistics')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'sightingsCount': 2,
      'birdersCount': 1,
    })

  def test_get_bird_statistics_when_blank(self):
    response = self.client.get('/birds/pica-pica/statistics')
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'sightingsCount': 0,
      'birdersCount': 0,
    })

  def test_get_bird_statistics_when_no_such_bird(self):
    response = self.client.get('/birds/pikachu/statistics')
    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
