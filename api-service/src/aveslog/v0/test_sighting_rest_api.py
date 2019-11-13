from datetime import date, time
from http import HTTPStatus

from flask import Response

from aveslog.test_util import AppTestCase
from aveslog.v0.error import ErrorCode


class TestGetSightings(AppTestCase):

  def setUp(self):
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))
    self.db_insert_sighting(2, 1, 1, date(2019, 8, 28), time(11, 52))
    self.db_insert_sighting(3, 2, 1, date(2019, 8, 28), time(11, 52))

  def test_get_sightings(self):
    response = self.get_with_access_token('/sighting', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 1,
          'birderId': 1,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        },
        {
          'id': 2,
          'birderId': 1,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        },
        {
          'id': 3,
          'birderId': 2,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        }
      ],
      'hasMore': False,
    })

  def test_get_sightings_with_valid_limit(self):
    response = self.get_with_access_token('/sighting?limit=1', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 1,
          'birderId': 1,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        }
      ],
      'hasMore': True,
    })

  def test_get_sightings_with_invalid_limit(self):
    response = self.get_with_access_token('/sighting?limit=0', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(response.json, {
      'error': 'limit-invalid',
    })

  def test_get_own_sightings_with_valid_auth_token(self):
    response = self.get_with_access_token('/profile/hulot/sighting',
                                          account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 1,
          'birderId': 1,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        },
        {
          'id': 2,
          'birderId': 1,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        }
      ],
      'hasMore': False,
    })

  def test_get_sightings_when_username_missing(self):
    response = self.get_with_access_token('/profile/godzilla/sighting',
                                          account_id=1)
    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

  def test_get_sightings_when_unauthorized(self):
    response = self.client.get('/profile/hulot/sighting')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.AUTHORIZATION_REQUIRED,
      'message': 'Authorization required',
    })

  def test_get_sightings_when_auth_token_invalid(self):
    headers = {'accessToken': 'i-am-not-a-valid-jwt-token'}

    response = self.client.get('/profile/hulot/sighting', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.ACCESS_TOKEN_INVALID,
      'message': 'Access token invalid',
    })

  def test_get_sightings_with_auth_token_for_other_account(self):
    response = self.get_with_access_token('/profile/dude/sighting',
                                          account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 3,
          'birderId': 2,
          'birdId': 'pica-pica',
          'date': '2019-08-28',
          'time': '11:52:00'
        }
      ],
      'hasMore': False,
    })


class TestGetSighting(AppTestCase):

  def test_get_sighting_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))

    response = self.get_with_access_token('/sighting/1', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'id': 1,
      'birderId': 1,
      'birdId': 'pica-pica',
      'date': '2019-08-28',
      'time': '11:52:00'
    })

  def test_get_sighting_when_not_authorized(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(12, 10))

    response = self.get_with_access_token('/sighting/2', account_id=1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class TestPostSighting(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')
    self.db_setup_account(1, 1, 'kenny', 'bostick!', 'kenny@mail.com')

  def test_post_sighting_when_everything_ok(self) -> None:
    token = self.create_access_token(1)

    response = self.post_sighting(1, token.jwt, 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertRegex(response.headers['Location'], '^\/sighting\/[0-9]+$')

  def test_post_sighting_when_birder_id_not_match_authentication(self) -> None:
    token = self.create_access_token(1)
    response = self.post_sighting(2, token.jwt, 'pica pica', '17:42')
    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_post_sighting_when_bird_not_present(self) -> None:
    token = self.create_access_token(1)
    response = self.post_sighting(1, token.jwt, 'pikachu', '17:42')
    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

  def test_post_sighting_when_no_time(self) -> None:
    token = self.create_access_token(1)

    response = self.post_sighting(1, token.jwt, 'pica pica')

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertRegex(response.headers['Location'], '^\/sighting\/[0-9]+$')

  def test_post_sighting_when_invalid_authentication_token(self) -> None:
    response = self.post_sighting(1, 'invalid token', 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.ACCESS_TOKEN_INVALID,
      'message': 'Access token invalid',
    })

  def post_sighting(
        self,
        birder_id: int,
        token: str,
        binomial_name: str,
        time: str = None
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
    return self.client.post(
      '/sighting',
      headers={
        'accessToken': token,
      },
      json=data,
    )


class TestDeleteSighting(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_insert_bird(1, 'Pica pica')

  def test_delete_sighting_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_sighting(1, 1, 1, date(2019, 9, 14), time(14, 25))
    self.db_insert_sighting(2, 1, 1, date(2019, 9, 14), time(14, 25))
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
    self.db_insert_sighting(1, 1, 1, date(2019, 9, 14), time(14, 25))

    response = self.delete_sighting('notOkToken', 1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_delete_sighting_when_authenticated_as_other_account(self):
    self.db_setup_account(1, 1, 'hulot', 'password', 'hulot@mail.com')
    self.db_insert_sighting(1, 1, 1, date(2019, 10, 4), time(16, 9))
    self.db_setup_account(2, 2, 'harry', 'wizardboy', 'harry@hogwarts.com')
    harry_token = self.create_access_token(2)

    response = self.delete_sighting(harry_token.jwt, 1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def delete_sighting(self,
        authentication_token: str,
        sighting_id: int) -> Response:
    resource = f'/sighting/{sighting_id}'
    headers = {'accessToken': authentication_token}
    return self.client.delete(resource, headers=headers)
