import datetime
from http import HTTPStatus
from typing import Optional
from datetime import timedelta
from flask import Response
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.authentication import AccessToken
from aveslog.v0.authentication import JwtFactory
from aveslog.test_util import AppTestCase
from aveslog.v0.error import ErrorCode


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


class TestPasswordReset(AppTestCase):

  def test_post_password_reset_email_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertIsNone(response.json)

  def test_post_password_reset_email_when_already_exist(self):
    self.db_setup_account(1, 1, 'george', 'costanza', 'tbone@mail.com')
    self.db_insert_locale(1, 'en')
    self.db_insert_password_reset_token(1, 'myToken')

    response = self.post_password_reset_email('tbone@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertIsNone(response.json)

  def test_post_password_reset_email_when_email_not_linked_with_account(self):
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(response.json, {
      'code': ErrorCode.EMAIL_MISSING,
      'message': 'E-mail not associated with any account',
    })

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

  def post_password_reset_email(self, email: str) -> Response:
    json = {'email': email}
    return self.client.post('/authentication/password-reset', json=json)

  def post_password_reset(self, token: str, password: str) -> Response:
    resource = f'/authentication/password-reset/{token}'
    return self.client.post(resource, json={'password': password})


class TestPasswordUpdate(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_setup_account(1, 1, 'hulot', 'oldPassword', 'hulot@mail.com')
    time_supplier = datetime.datetime.utcnow
    jwt_factory = JwtFactory(self._app.secret_key)
    self.token_factory = AuthenticationTokenFactory(jwt_factory, time_supplier)

  def test_post_password_update_when_ok(self) -> None:
    token = self.token_factory.create_access_token(1, timedelta(1))

    response = self.post_password_update(token.jwt, 'oldPassword',
      'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

  def test_post_password_update_when_token_missing(self) -> None:
    response = self.post_password_update(None, 'oldPassword', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.AUTHORIZATION_REQUIRED,
      'message': 'Authorization required',
    })

  def test_post_password_update_when_token_invalid(self) -> None:
    response = self.post_password_update('invalid', 'oldPassword',
      'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.ACCESS_TOKEN_INVALID,
      'message': 'Access token invalid',
    })

  def test_post_password_update_when_token_expired(self) -> None:
    expiration = timedelta(seconds=-1)
    token = self.token_factory.create_access_token(1, expiration)

    response = self.post_password_update(token.jwt, 'oldPassword',
      'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.ACCESS_TOKEN_EXPIRED,
      'message': 'Access token expired',
    })

  def test_post_password_update_when_old_password_incorrect(self) -> None:
    token = self.token_factory.create_access_token(1, timedelta(1))

    response = self.post_password_update(token.jwt, 'incorrect', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'code': ErrorCode.OLD_PASSWORD_INCORRECT,
      'message': 'Old password incorrect',
    })

  def test_post_password_update_when_new_password_invalid(self) -> None:
    token = self.token_factory.create_access_token(1, timedelta(1))

    response = self.post_password_update(token.jwt, 'oldPassword', 'invalid')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(response.json, {
      'code': ErrorCode.PASSWORD_INVALID,
      'message': 'New password invalid',
    })

  def post_password_update(self,
        token: Optional[str],
        old_password: str,
        new_password: str) -> Response:
    resource = '/authentication/password'
    headers = {'accessToken': token} if token else {}
    json = {'oldPassword': old_password, 'newPassword': new_password}
    return self.client.post(resource, headers=headers, json=json)


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
