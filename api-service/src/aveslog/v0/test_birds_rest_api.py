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
    self.db_insert_bird_common_name(1, 1, 1, 'Skata')
    self.db_insert_bird_common_name(2, 1, 2, 'Eurasian Magpie')
    self.db_insert_bird_common_name(3, 1, 3, '까치')
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


class TestGetBirdsCommonNames(AppTestCase):

  def test_get_bird_common_names_when_ok(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_locale(1, 'sv')
    self.db_insert_locale(2, 'en')
    self.db_insert_locale(3, 'ko')
    self.db_insert_bird_common_name(1, 1, 1, 'Skata')
    self.db_insert_bird_common_name(2, 1, 2, 'Eurasian Magpie')
    self.db_insert_bird_common_name(3, 1, 3, '까치')
    response = self.client.get('/birds/pica-pica/common-names')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.headers['Cache-Control'], 'max-age=300')
    self.assertDictEqual(response.json, {
      'items': [
        {'id': 1, 'locale': 'sv', 'name': 'Skata'},
        {'id': 2, 'locale': 'en', 'name': 'Eurasian Magpie'},
        {'id': 3, 'locale': 'ko', 'name': '까치'},
      ],
    })


class TestPostBirdsCommonName(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_insert_locale(1, 'sv')
    self.db_insert_bird(2, 'Pica pica')
    self.db_setup_account(3, 4, 'hulot', 'password', 'hulot@mail.com')

  def test_create_common_name_when_ok(self):
    self._setup_correct_permissions()
    token = self.create_access_token(4)

    response = self.client.post(
      '/birds/pica-pica/common-names',
      headers={
        'accessToken': token.jwt,
      },
      json={
        'locale': 'sv', 'name': 'Skata'
      })

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertRegex(response.headers['Location'],
      '^\/birds\/pica-pica\/common-names\/[0-9]+$')
    common_name_response = self.client.get(response.headers['Location'])
    self.assertDictEqual(common_name_response.json, {
      'id': 1, 'locale': 'sv', 'name': 'Skata'
    })

  def test_post_common_name_when_bird_id_missing(self):
    self._setup_correct_permissions()
    token = self.create_access_token(4)

    response = self.client.post(
      '/birds/pica-poci/common-names',
      headers={
        'accessToken': token.jwt,
      },
      json={
        'locale': 'sv', 'name': 'Skata'
      })

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

  def test_post_common_name_when_locale_invalid(self):
    self._setup_correct_permissions()
    token = self.create_access_token(4)

    response = self.client.post(
      '/birds/pica-pica/common-names',
      headers={
        'accessToken': token.jwt,
      },
      json={
        'locale': 'dk', 'name': 'Skata'
      })

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

  def test_create_common_name_without_permitted_role(self):
    self.db_insert_role(5, 'permitted')
    self.db_insert_resource_permission(6, '^/birds/[^/]+/common-names$', 'POST')
    self.db_insert_role_resource_permission(5, 6)
    # note permitted role not given to account
    token = self.create_access_token(4)

    response = self.client.post(
      '/birds/pica-pica/common-names',
      headers={
        'accessToken': token.jwt,
      },
      json={
        'locale': 'sv', 'name': 'Skata'
      })

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_create_common_name_without_correct_permission(self):
    self.db_insert_role(5, 'permitted')
    # note resource regex of permission below doesn't match resource
    self.db_insert_resource_permission(6, '^/birds/picapica/common-names$',
      'POST')
    self.db_insert_role_resource_permission(5, 6)
    self.db_insert_account_role(4, 5)
    token = self.create_access_token(4)

    response = self.client.post(
      '/birds/pica-pica/common-names',
      headers={
        'accessToken': token.jwt,
      },
      json={
        'locale': 'sv', 'name': 'Skata'
      })

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def _setup_correct_permissions(self):
    self.db_insert_role(5, 'permitted')
    self.db_insert_resource_permission(6, '^/birds/[^/]+/common-names$', 'POST')
    self.db_insert_role_resource_permission(5, 6)
    self.db_insert_account_role(4, 5)
