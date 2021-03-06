import datetime
from http import HTTPStatus
from flask import Response, current_app
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.authentication import AccessToken
from aveslog.v0.authentication import JwtFactory
from aveslog.test_util import AppTestCase
from aveslog.v0.error import ErrorCode
from aveslog.v0.link import LinkFactory


class TestPostRefreshToken(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')

  def test_post_refresh_token_when_ok(self) -> None:
    response = self.post_refresh_token('george', 'costanza')

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertIn('id', response.json)
    self.assertIn('refreshToken', response.json)
    self.assertIn('expirationDate', response.json)

  def test_post_refresh_token_when_username_differently_cased(self) -> None:
    response = self.post_refresh_token('GeOrGe', 'costanza')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.CREDENTIALS_INCORRECT,
      'message': 'Credentials incorrect',
    })

  def test_post_refresh_token_when_incorrect_username(self) -> None:
    response = self.post_refresh_token('tbone', 'costanza')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.CREDENTIALS_INCORRECT,
      'message': 'Credentials incorrect',
    })

  def test_post_refresh_token_when_incorrect_password(self) -> None:
    response = self.post_refresh_token('george', 'festivus')
    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.CREDENTIALS_INCORRECT,
      'message': 'Credentials incorrect',
    })


class TestGetAccessToken(AppTestCase):

  def test_get_access_token_when_ok(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    post_refresh_token_response = self.post_refresh_token('george', 'costanza')
    refresh_token = post_refresh_token_response.json['refreshToken']
    headers = {'refreshToken': refresh_token}

    response = self.client.get('/authentication/access-token', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertIn('jwt', response.json)
    self.assertIn('expiresIn', response.json)

  def test_get_access_token_when_no_refresh_token(self):
    response = self.client.get('/authentication/access-token')
    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_get_access_token_when_refresh_token_removed_from_database(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    post_refresh_token_response = self.post_refresh_token('george', 'costanza')
    json = post_refresh_token_response.json
    headers = {'refreshToken': (json['refreshToken'])}
    self.db_delete_refresh_token(json['id'])

    response = self.client.get('/authentication/access-token', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_get_access_token_when_refresh_token_invalid(self):
    headers = {'refreshToken': 'asdfasdf.asdfasdf.asdfasdf'}
    response = self.client.get('/authentication/access-token', headers=headers)
    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def test_get_access_token_when_refresh_token_expired(self):
    jwt_factory = JwtFactory(self._app.secret_key)
    time_supplier = lambda: datetime.datetime(2015, 1, 1)
    token_factory = AuthenticationTokenFactory(jwt_factory, time_supplier)
    refresh_token = token_factory.create_refresh_token(1)
    headers = {'refreshToken': (refresh_token.token)}

    response = self.client.get('/authentication/access-token', headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class TestCredentialsRecovery(AppTestCase):

  def test_post_credentials_recovery_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    password_reset_tokens = self.db_get_password_reset_tokens()
    link_factory = LinkFactory(
      current_app.config['EXTERNAL_HOST'],
      current_app.config['FRONTEND_HOST'],
    )
    self.assertEqual(len(password_reset_tokens), 1)
    link = link_factory.create_frontend_link(
      f'/authentication/password-reset/{password_reset_tokens[0][1]}')
    self.assertListEqual(self.dispatched_mails, [
      {
        'body':
          'Having trouble logging into your aveslog.com account? Your username '
          'is hulot, and here\'s a password reset link if you need one: '
          f'{link}',
        'recipient': 'hulot@mail.com',
        'subject': 'Aveslog Credentials Recovery',
      }
    ])
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertIsNone(response.json)

  def test_post_credentials_recovery_when_already_exist(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    self.db_insert_locale(1, 'en')
    self.db_insert_password_reset_token(1, 'myToken')

    response = self.post_password_reset_email('tbone@mail.com')

    password_reset_tokens = self.db_get_password_reset_tokens()
    link_factory = LinkFactory(
      current_app.config['EXTERNAL_HOST'],
      current_app.config['FRONTEND_HOST'],
    )
    self.assertEqual(len(password_reset_tokens), 1)
    link = link_factory.create_frontend_link(
      f'/authentication/password-reset/{password_reset_tokens[0][1]}')
    self.assertListEqual(self.dispatched_mails, [
      {
        'body':
          'Having trouble logging into your aveslog.com account? Your username '
          'is george, and here\'s a password reset link if you need one: '
          f'{link}',
        'recipient': 'tbone@mail.com',
        'subject': 'Aveslog Credentials Recovery',
      }
    ])
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertIsNone(response.json)

  def test_post_credentials_recovery_when_email_not_linked_with_account(self):
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    self.assertFalse(self.dispatched_mails)
    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(response.json, {
      'code': ErrorCode.EMAIL_MISSING,
      'message': 'E-mail not associated with any account',
    })

  def post_password_reset_email(self, email: str) -> Response:
    json = {'email': email}
    return self.client.post('/authentication/credentials-recovery', json=json)


class TestPasswordReset(AppTestCase):

  def test_post_password_reset_when_password_reset_not_first_created(self):
    response = self.post_password_reset('myToken', 'myNewPassword')

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    self.assertIsNone(response.json)

  def test_post_password_reset_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_password_reset_token(1, 'myToken')

    response = self.post_password_reset('myToken', 'myNewPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertIsNone(response.json)

  def post_password_reset(self, token: str, password: str) -> Response:
    resource = f'/authentication/password-reset/{token}'
    return self.client.post(resource, json={'password': password})


class TestDeleteRefreshToken(AppTestCase):

  def test_delete_refresh_token_when_ok(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    refresh_token = self.post_refresh_token('george', 'costanza').json
    access_token = self.create_access_token(1)
    refresh_token_id = refresh_token['id']

    response = self.delete_refresh_token(refresh_token_id, access_token)

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

  def test_delete_refresh_token_when_already_missing(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    access_token = self.create_access_token(1)

    response = self.delete_refresh_token(1, access_token)

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

  def test_delete_refresh_token_when_not_your_own(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    self.db_setup_account(2, 2, 'kenny', 'bostick!', 'birds@mail.com')
    kenny_refresh_token = self.post_refresh_token('kenny', 'bostick!').json
    george_access_token = self.create_access_token(1)

    response = self.delete_refresh_token(kenny_refresh_token['id'],
      george_access_token)

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

  def delete_refresh_token(self, refresh_token_id: int,
        access_token: AccessToken) -> Response:
    return self.client.delete(
      f'/authentication/refresh-token/{refresh_token_id}',
      headers={'accessToken': access_token.jwt})
