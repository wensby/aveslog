import datetime
import json
from http import HTTPStatus
from datetime import timedelta

from birding import AuthenticationTokenFactory, JwtFactory
from test_util import AppTestCase


class TestGetActiveAccounts(AppTestCase):

  def test_get_active_accounts_ok_when_authenticated(self):
    self.db_setup_account(1, 1, 'hulot', 'password', 'hulot@mail.com')
    token = self.get_authentication_token('hulot', 'password')

    response = self.client.get('/account', headers={'authToken': token})

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': [
        {
          'username': 'hulot',
          'personId': 1,
        },
      ],
    })


class TestAccount(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    secret_key = self._app.secret_key
    time_supplier = datetime.datetime.utcnow
    self.jwt_factory = JwtFactory(secret_key)
    self.token_factory = AuthenticationTokenFactory(self.jwt_factory, time_supplier)

  def test_get_account_when_authenticated_account_disappears(self):
    token = self.token_factory.create_authentication_token(1)

    response = self.get_own_account(token)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'account missing',
    })

  def test_get_account_when_no_authentication_token(self):
    response = self.get_own_account(None)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'authentication token required')

  def test_get_account_when_authentication_token_invalid(self):
    response = self.get_own_account('invalid')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'authentication token invalid')

  def test_get_account_when_authentication_token_expired(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    expiration = timedelta(seconds=-1)
    token = self.token_factory.create_authentication_token(1, expiration)

    response = self.get_own_account(token)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'authentication token expired')

  def test_get_account_when_authentication_token_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    token = self.token_factory.create_authentication_token(1)

    response = self.get_own_account(token)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    self.assertEqual(data['account']['username'], 'hulot')
    self.assertEqual(data['account']['personId'], 1)

  def get_own_account(self, token):
    if not token:
      return self.client.get('/account/me')
    else:
      return self.client.get('/account/me', headers={'authToken': token})
