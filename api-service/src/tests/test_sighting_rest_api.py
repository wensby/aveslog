from datetime import date, time
from http import HTTPStatus

from flask import Response

from test_util import AppTestCase


class TestGetSighting(AppTestCase):

  def test_get_sighting_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))
    token = self.get_authentication_token('hulot', 'myPassword')
    headers = {'authToken': token}

    response = self.client.get('/sighting/1', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'sightingId': 1,
        'personId': 1,
        'birdId': 1,
        'date': '2019-08-28',
        'time': '11:52:00'
      },
    })

  def test_get_sighting_when_not_authorized(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(12, 10))
    token = self.get_authentication_token('hulot', 'myPassword')
    headers = {'authToken': token}

    response = self.client.get('/sighting/2', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class TestGetSightings(AppTestCase):

  def test_get_own_sightings_with_valid_auth_token(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(12, 10))
    token = self.get_authentication_token('hulot', 'myPassword')
    headers = {'authToken': token}

    response = self.client.get('/profile/hulot/sighting', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'sightings': [
          {
            'sightingId': 1,
            'personId': 1,
            'birdId': 1,
            'date': '2019-08-28',
            'time': '11:52:00'
          }
        ]
      }
    })

  def test_get_sightings_when_username_missing(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    token = self.get_authentication_token('hulot', 'myPassword')
    headers = {'authToken': token}

    response = self.client.get('/profile/godzilla/sighting', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

  def test_get_sightings_when_unauthorized(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))

    response = self.client.get('/profile/hulot/sighting')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'authentication token required',
    })

  def test_get_sightings_when_auth_token_invalid(self):
    headers = {'authToken': 'i-am-not-a-valid-jwt-token'}

    response = self.client.get('/profile/hulot/sighting', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'authentication token invalid',
    })

  def test_get_sightings_with_auth_token_for_other_account(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_setup_account(2, 2, 'dude', 'myPassword', 'dude@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(12, 10))
    token = self.get_authentication_token('hulot', 'myPassword')
    headers = {'authToken': token}

    response = self.client.get('/profile/dude/sighting', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'sightings': [
          {
            'sightingId': 2,
            'personId': 2,
            'birdId': 1,
            'date': '2019-08-28',
            'time': '12:10:00'
          }
        ]
      }
    })


class TestPostSighting(AppTestCase):

  def test_post_sighting_when_everything_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    token = self.get_authentication_token('hulot', 'myPassword')

    response = self.post_sighting(1, token, 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {'status': 'success'})

  def test_post_sighting_when_person_id_not_match_authentication(self) -> None:
    self.db_setup_account(1, 1, 'kenny', 'bostick!', 'kenny@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    token = self.get_authentication_token('kenny', 'bostick!')

    response = self.post_sighting(2, token, 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_post_sighting_when_bird_not_present(self) -> None:
    self.db_setup_account(1, 1, 'kenny', 'bostick!', 'kenny@mail.com')
    token = self.get_authentication_token('kenny', 'bostick!')

    response = self.post_sighting(1, token, 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

  def test_post_sighting_when_no_time(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_bird(1, 'Pica pica')
    token = self.get_authentication_token('hulot', 'myPassword')

    response = self.post_sighting(1, token, 'pica pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {'status': 'success'})

  def test_post_sighting_when_invalid_authentication_token(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_bird(1, 'Pica pica')

    response = self.post_sighting(1, 'invalid token', 'pica pica', '17:42')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'authentication token invalid',
    })

  def post_sighting(
        self,
        person_id: int,
        token: str,
        binomial_name: str,
        time: str = None
  ) -> Response:
    data = {
      'person': {
        'id': person_id
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
        'authToken': token,
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
    authentication_token = self.get_authentication_token('hulot', 'myPassword')

    response = self.delete_sighting(authentication_token, 1)

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

  def test_delete_sighting_when_not_exist(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    authentication_token = self.get_authentication_token('hulot', 'myPassword')

    response = self.delete_sighting(authentication_token, 1)

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
    harry_token = self.get_authentication_token('harry', 'wizardboy')

    response = self.delete_sighting(harry_token, 1)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def delete_sighting(self,
        authentication_token: str,
        sighting_id: int) -> Response:
    resource = f'/sighting/{sighting_id}'
    headers = {'authToken': authentication_token}
    return self.client.delete(resource, headers=headers)
