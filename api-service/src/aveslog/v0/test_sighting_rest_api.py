import re
from datetime import date, time, datetime
from http import HTTPStatus

from flask import Response

from aveslog.test_util import AppTestCase
from aveslog.v0.error import ErrorCode


class TestGetSightings(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')
    self.db_setup_account(2, 3, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(4, 5, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_position(6, (47.240055, 2.2783327))
    self.db_insert_position(7, (37.5665, 126.9780))
    self.db_insert_sighting(8, 2, 1, date(2019, 8, 28), time(11, 52), 6)
    self.db_insert_sighting(9, 2, 1, date(2019, 8, 28), time(11, 52), None)
    self.db_insert_sighting(10, 4, 1, date(2019, 8, 28), time(11, 52), 7)

  def test_get_sightings(self):
    response = self.get_with_access_token('/sightings', account_id=3)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'items': [
        {
          'id': 8,
          'birderId': 2,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00',
          'position': {
            'lat': 47.240055,
            'lon': 2.2783327,
          }
        },
        {
          'id': 9,
          'birderId': 2,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        },
        {
          'id': 10,
          'birderId': 4,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00',
          'position': {
            'lat': 37.5665,
            'lon': 126.9780,
          }
        }
      ],
      'hasMore': False,
    })

  def test_get_sightings_with_valid_limit(self):
    response = self.get_with_access_token('/sightings?limit=1', account_id=3)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'items': [
        {
          'id': 8,
          'birderId': 2,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00',
          'position': {
            'lat': 47.240055,
            'lon': 2.2783327,
          }
        }
      ],
      'hasMore': True,
    })

  def test_get_sightings_with_invalid_limit(self):
    response = self.get_with_access_token('/sightings?limit=0', account_id=3)

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(response.json, {
      'error': 'limit-invalid',
    })

  def test_get_sightings_when_username_missing(self):
    response = self.get_with_access_token('/profile/godzilla/sightings',
      account_id=3)
    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

  def test_get_sightings_when_unauthorized(self):
    response = self.client.get('/birders/2/sightings')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.AUTHORIZATION_REQUIRED,
      'message': 'Authorization required',
    })

  def test_get_sightings_when_auth_token_invalid(self):
    headers = {'accessToken': 'i-am-not-a-valid-jwt-token'}

    response = self.client.get('/birders/2/sightings', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.ACCESS_TOKEN_INVALID,
      'message': 'Access token invalid',
    })

  def test_get_sightings_with_auth_token_for_other_account(self):
    response = self.get_with_access_token('/birders/4/sightings', account_id=3)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'items': [
        {
          'id': 10,
          'birderId': 4,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00',
          'position': {
            'lat': 37.5665,
            'lon': 126.9780,
          }
        }
      ],
      'hasMore': False,
    })


class TestGetSighting(AppTestCase):

  def test_get_sighting_when_ok(self):
    self.db_insert_locale(4, 'en')
    self.db_insert_bird(8, 'Pica pica')
    self.db_insert_position(15, (47.240055, 2.2783327))
    self.db_insert_position_name(16, 15, 4, 21,
      "La Prinquette, Bourges, Cher, Centre-Val de Loire, France métropolitaine, France",
      datetime(2019, 12, 17, 17, 48))
    self.db_setup_account(23, 42, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_sighting(48, 23, 8, date(2019, 8, 28), time(11, 52), 15)

    response = self.get_with_access_token('/sightings/48', account_id=42)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'id': 48,
      'birderId': 23,
      'birdId': 'pica-pica',
      'date': '2019-08-28',
      'time': '11:52:00',
      'position': {
        'name': 'La Prinquette, Bourges, Cher, Centre-Val de Loire, France métropolitaine, France',
        'lat': 47.240055,
        'lon': 2.2783327,
      },
    })

  def test_get_sighting_when_not_authorized(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_position(4, (47.240055, 2.2783327))
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(12, 10), 4)

    response = self.get_with_access_token('/sightings/2', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class TestPostSighting(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_insert_locale(1, 'en')
    self.db_insert_bird(1, 'Pica pica')
    self.db_setup_account(1, 1, 'kenny', 'bostick!', 'kenny@mail.com')

  def test_post_sighting_when_everything_ok(self):
    access_token = self.create_access_token(1).jwt

    sighting_post_response = self.post_sighting(
      access_token,
      1,
      'pica pica',
      '17:42',
      (64.145981, -21.9422367),
    )

    self.assertEqual(sighting_post_response.status_code, HTTPStatus.CREATED)
    sighting_id = get_created_sighting_id(sighting_post_response)
    sighting_url = f'/sightings/{sighting_id}'
    sighting = self.get_with_access_token(sighting_url, account_id=1)
    self.assertDictEqual(sighting.json, {
      'id': sighting_id,
      'birderId': 1,
      'birdId': 'pica-pica',
      'date': '2019-09-11',
      'time': '17:42:00',
      'position': {
        'name': '(64.145981, -21.9422367) name',
        'lat': 64.145981,
        'lon': -21.9422367
      }
    })

  def test_post_sighting_when_birder_id_not_match_authentication(self) -> None:
    token = self.create_access_token(1)
    position = (64.145981, -21.9422367)

    response = self.post_sighting(token.jwt, 2, 'pica pica', '17:42', position)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_post_sighting_when_bird_not_present(self) -> None:
    token = self.create_access_token(1)
    position = (64.145981, -21.9422367)

    response = self.post_sighting(token.jwt, 1, 'pikachu', '17:42', position)

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

  def test_post_sighting_when_no_time(self) -> None:
    token = self.create_access_token(1)
    position = (64.145981, -21.9422367)

    response = self.post_sighting(token.jwt, 1, 'pica pica', position=position)

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertRegex(response.headers['Location'], '^\/sightings\/[0-9]+$')

  def test_post_sighting_when_no_position(self) -> None:
    token = self.create_access_token(1)

    response = self.post_sighting(token.jwt, 1, 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertRegex(response.headers['Location'], '^\/sightings\/[0-9]+$')

  def test_post_sighting_when_invalid_authentication_token(self) -> None:
    position = (64.145981, -21.9422367)
    jwt = 'invalid token'

    response = self.post_sighting(jwt, 1, 'pica pica', '17:42', position)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.ACCESS_TOKEN_INVALID,
      'message': 'Access token invalid',
    })

  def post_sighting(
        self,
        access_token: str,
        birder_id: int,
        binomial_name: str,
        time: str = None,
        position: tuple = None,
  ) -> Response:
    data = {
      'birder': {
        'id': birder_id
      },
      'bird': {
        'binomialName': binomial_name,
      },
      'date': '2019-09-11',
    }
    if time:
      data['time'] = time
    if position:
      data['position'] = {
        'lat': position[0],
        'lon': position[1],
      }
    return self.client.post(
      '/sightings',
      headers={
        'accessToken': access_token,
      },
      json=data,
    )


class TestDeleteSighting(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')

  def test_delete_sighting_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_position(4, (47.240055, 2.2783327))
    self.db_insert_position(8, (37.5665, 126.9780))
    self.db_insert_sighting(1, 1, 1, date(2019, 9, 14), time(14, 25), 4)
    self.db_insert_sighting(2, 1, 1, date(2019, 9, 14), time(14, 25), 8)
    authentication_token = self.create_access_token(1)

    response = self.delete_sighting(authentication_token.jwt, 1)

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
    self.assertEqual(len(self.db_get_sighting_rows()), 1)

  def test_delete_sighting_when_not_exist(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    authentication_token = self.create_access_token(1)

    response = self.delete_sighting(authentication_token.jwt, 1)

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

  def test_delete_sighting_when_not_authorized(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_position(4, (47.240055, 2.2783327))
    self.db_insert_sighting(1, 1, 1, date(2019, 9, 14), time(14, 25), 4)

    response = self.delete_sighting('notOkToken', 1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_delete_sighting_when_authenticated_as_other_account(self):
    self.db_setup_account(1, 1, 'hulot', 'password', 'hulot@mail.com')
    self.db_insert_position(4, (47.240055, 2.2783327))
    self.db_insert_sighting(1, 1, 1, date(2019, 10, 4), time(16, 9), 4)
    self.db_setup_account(2, 2, 'harry', 'wizardboy', 'harry@hogwarts.com')
    harry_token = self.create_access_token(2)

    response = self.delete_sighting(harry_token.jwt, 1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def delete_sighting(self,
        authentication_token: str,
        sighting_id: int) -> Response:
    resource = f'/sightings/{sighting_id}'
    headers = {'accessToken': authentication_token}
    return self.client.delete(resource, headers=headers)


def get_created_sighting_id(response):
  pattern = re.compile('^/sightings/([0-9]+)$')
  sighting_id = int(pattern.match(response.headers['Location']).group(1))
  return sighting_id
