from datetime import date, time

from test_util import AppTestCase
from http import HTTPStatus


class TestGetPerson(AppTestCase):

  def test_get_person(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    token = self.create_access_token(1)
    headers = {'accessToken': token.jwt}

    response = self.client.get('/person/1', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'id': 1,
      'name': 'hulot',
    })

class TestGetPersonsSightings(AppTestCase):

  def test_get_person_sightings(self):
    self.db_insert_bird(1, 'Pica pica')
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_sighting(1, 1, 1, date(2019, 8, 28), time(11, 52))
    token = self.create_access_token(1)
    headers = {'accessToken': token.jwt}

    response = self.client.get('/birders/1/sightings', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'items': [
        {
          'id': 1,
          'personId': 1,
          'birdId': 1,
          'date': '2019-08-28',
          'time': '11:52:00',
        }
      ],
      'hasMore': False,
    })