import json
from http import HTTPStatus

from test_util import AppTestCase


class TestLogin(AppTestCase):

  def test_login_when_correct_credentials(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.db_insert_password(4, 'myPassword')

    data = {'username': 'myUsername', 'password': 'myPassword'}
    response = self.client.post('/v2/authentication/login', data=data)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    self.assertEqual(data['message'], 'Successfully logged in.')
    self.assertIn('auth_token', data)

  def test_login_when_incorrect_credentials(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.db_insert_password(4, 'myPassword')

    data = {'username': 'somethingElse', 'password': 'notGood'}
    response = self.client.post('/v2/authentication/login', data=data)

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'Try again')
    self.assertNotIn('auth_token', data)
