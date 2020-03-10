from datetime import date, time

from aveslog.test_util import AppTestCase
from http import HTTPStatus


class TestGetBirder(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')

  def test_get_birder(self):
    response = self.get_with_access_token('/birders/1', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.headers['Cache-Control'], 'max-age=300')
    self.assertEqual(response.json, {
      'id': 1,
      'name': 'hulot',
    })

  def test_get_birder_when_missing(self):
    response = self.get_with_access_token('/birders/2', account_id=1)
    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestGetBirderConnections(AppTestCase):

  def test_get_authenticated_accounts_birder_connections(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.db_insert_birder_connection(1, 2)
    token = self.create_access_token(1)

    uri = '/birders/1/birder-connections'
    response = self.client.get(uri, headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'items': [
        {
          'birderId': 2
        }
      ],
      "hasMore": False,
    })

  def test_get_birder_connections_without_proper_authentication(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.db_insert_birder_connection(2, 1)
    token = self.create_access_token(1)

    uri = '/birders/2/birder-connections'
    response = self.client.get(uri, headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertIsNone(response.json)


class TestGetBirders(AppTestCase):

  def test_get_birders_when_ok(self):
    token = self.create_access_token(1)
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_birder(2, 'Kenny Bostick')
    response = self.client.get('/birders', headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertNotIn('Cache-Control', response.headers)
    self.assertDictEqual(response.json, {
      'items': [
        {
          'id': 1,
          'name': 'hulot',
        },
        {
          'id': 2,
          'name': 'Kenny Bostick',
        }
      ],
      'hasMore': False,
    })


class TestGetBirderSightings(AppTestCase):

  def test_get_birder_sightings(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'george', 'costanza', 'tbone@mail.com')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52), None)
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(11, 52), None)

    response = self.get_with_access_token('/birders/1/sightings', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 1,
          'birderId': 1,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00',
        }
      ],
      'hasMore': False,
    })
