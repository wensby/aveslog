from datetime import date, time, datetime

from aveslog.test_util import AppTestCase
from http import HTTPStatus

from aveslog.v0 import ErrorCode


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
    self.db_insert_birder_connection(1, 1, 2)
    token = self.create_access_token(1)

    uri = '/birders/1/birder-connections'
    response = self.client.get(uri, headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'items': [
        {
          'id': 1,
          'secondaryBirderId': 2,
        }
      ],
      "hasMore": False,
    })

  def test_get_birder_connections_without_proper_authentication(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.db_insert_birder_connection(1, 2, 1)
    token = self.create_access_token(1)

    uri = '/birders/2/birder-connections'
    response = self.client.get(uri, headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertIsNone(response.json)


class TestPostBirderConnection(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.access_token = self.create_access_token(1).jwt

  def test_post_birder_connection_when_ok(self):
    json = {'secondaryBirderId': 2}
    headers = {'accessToken': self.access_token}

    response = self.post('/birders/1/birder-connections', headers, json)

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertEqual(response.headers['Location'], '/birder-connections/1')
    birder_connections = self.db_get_birder_connections()
    self.assertEqual(len(birder_connections), 1)
    self.assertEqual(birder_connections[0][0], 1)
    self.assertEqual(birder_connections[0][1], 1)
    self.assertEqual(birder_connections[0][2], 2)
    self.assertIsInstance(birder_connections[0][3], datetime)

  def test_post_birder_connection_when_field_invalid_format(self):
    json = {'secondaryBirderId': '2'}
    headers = {'accessToken': self.access_token}

    response = self.post('/birders/1/birder-connections', headers, json)

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertDictEqual(response.json, {
      'code': ErrorCode.VALIDATION_FAILED,
      'message': 'Validation failed',
      'errors': [
        {
          'code': ErrorCode.INVALID_FIELD_FORMAT,
          'field': 'secondaryBirderId',
          'message': 'Identifier need to be a positive integer'
        },
      ]
    })

  def test_post_birder_connection_with_oneself(self):
    json = {'secondaryBirderId': 1}
    headers = {'accessToken': self.access_token}

    response = self.post('/birders/1/birder-connections', headers, json)

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertDictEqual(response.json, {
      'code': ErrorCode.VALIDATION_FAILED,
      'message': 'Validation failed',
      'errors': [
        {
          'code': ErrorCode.SECONDARY_BIRDER_ID_INVALID,
          'field': 'secondaryBirderId',
          'message': 'Birder may not create connection with itself'
        },
      ]
    })

  def test_post_birder_connection_with_wrong_account(self):
    json = {'secondaryBirderId': 1}
    headers = {'accessToken': self.access_token}

    response = self.post('/birders/2/birder-connections', headers, json)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def post(self, uri, headers, json):
    return self.client.post(uri, json=json, headers=headers)


class TestDeleteBirdersBirderConnection(AppTestCase):

  def test_delete_birders_birder_connection_when_ok(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.db_insert_birder_connection(1, 1, 2)
    token = self.create_access_token(1)
    uri = '/birders/1/birder-connections/1'
    headers = {'accessToken': token.jwt}

    response = self.client.delete(uri, headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
    birder_connections = self.db_get_birder_connections()
    self.assertEqual(len(birder_connections), 0)


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
