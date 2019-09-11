from datetime import date, time
from http import HTTPStatus

from flask import Response

from test_util import AppTestCase


class TestGetSightings(AppTestCase):

  def test_get_own_sightings_with_valid_auth_token(self):
    self.db_insert_person(1)
    self.db_insert_person(2)
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', 1, None)
    self.db_insert_account(2, 'dude', 'dude@mail.com', 2, None)
    self.db_insert_password(1, 'myPassword')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))
    self.db_insert_sighting(2, 2, 1, date(2019, 8, 28), time(12, 10))
    token = self.get_authentication_token('hulot', 'myPassword')
    headers = {'authToken': token}

    response = self.client.get('/v2/profile/hulot/sighting', headers=headers)

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

  def test_get_sightings_when_unauthorized(self):
    self.db_insert_person(1)
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', 1, None)
    self.db_insert_password(1, 'myPassword')
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))

    response = self.client.get('/v2/profile/hulot/sighting')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'You are not authorized to get these sightings',
    })

  def test_get_sightings_when_auth_token_invalid(self):
    headers = {'authToken': 'i-am-not-a-valid-jwt-token'}

    response = self.client.get('/v2/profile/hulot/sighting', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'You are not authorized to get these sightings',
    })


class TestAddSighting(AppTestCase):

  def test_add_sighting_when_everything_ok(self):
    self.db_insert_person(1)
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', 1, None)
    self.db_insert_password(1, 'myPassword')
    self.db_insert_bird(1, 'Pica pica')
    token = self.get_authentication_token('hulot', 'myPassword')

    response = self.post_sighting(token, 'pica pica')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {'status': 'success'})

  def test_add_sighting_when_invalid_authentication_token(self):
    self.db_insert_person(1)
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', 1, None)
    self.db_insert_password(1, 'myPassword')
    self.db_insert_bird(1, 'Pica pica')

    response = self.post_sighting('invalid token', 'pica pica')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {'status': 'failure'})

  def post_sighting(self, token: str, binomial_name: str) -> Response:
    return self.client.post(
      '/v2/sighting',
      headers={
        'authToken': token,
      },
      json={
        'person': {
          'id': 1
        },
        'bird': {
          'binomialName': binomial_name,
        },
        'date': '2019-09-11',
        'time': '17:42'
      })
