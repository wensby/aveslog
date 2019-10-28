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
      'personId': 1,
      'name': 'hulot',
    })
