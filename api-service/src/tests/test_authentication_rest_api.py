import datetime
from http import HTTPStatus
from typing import Optional
from datetime import timedelta
from flask import Response
from birding.authentication import AuthenticationTokenFactory
from test_util import AppTestCase


class TestLogin(AppTestCase):

  def test_get_token_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')

    response = self.get_authentication_token('hulot', 'myPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json['status'], 'success')
    self.assertEqual(response.json['message'], 'Successfully logged in.')
    self.assertIn('authToken', response.json)

  def test_get_token_when_incorrect_credentials(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')

    response = self.get_authentication_token('somethingElse', 'notGood')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'Try again',
    })

  def get_authentication_token(self, username: str, password: str) -> Response:
    resource = '/authentication/token'
    query = f'username={username}&password={password}'
    return self.client.get(f'{resource}?{query}')


class TestPasswordReset(AppTestCase):

  def test_post_password_reset_email_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'message': 'Password reset link sent to e-mail',
    })

  def test_post_password_reset_email_when_email_not_linked_with_account(self):
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'E-mail not associated with any account',
    })

  def test_post_password_reset_when_password_reset_not_first_created(self):
    response = self.post_password_reset('myToken', 'myNewPassword')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'Password reset token not recognized'
    })

  def test_post_password_reset_when_ok(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_password_reset_token(1, 'myToken')

    response = self.post_password_reset('myToken', 'myNewPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'message': 'Password reset successfully',
    })

  def post_password_reset_email(self, email: str) -> Response:
    json = {'email': email}
    return self.client.post('/authentication/password-reset', json=json)

  def post_password_reset(self, token: str, password: str) -> Response:
    resource = f'/authentication/password-reset/{token}'
    return self.client.post(resource, json={'password': password})


class TestRegistration(AppTestCase):

  def test_post_registration_email_when_ok(self):
    self.db_insert_locale(1, 'en')

    response = self.post_registration_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
    })

  def test_post_registration_email_when_email_invalid(self):
    self.db_insert_locale(1, 'en')

    response = self.post_registration_email('hulot')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'Email invalid',
    })

  def test_post_registration_email_when_email_taken(self):
    self.db_insert_locale(1, 'en')
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')

    response = self.post_registration_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'Email taken',
    })

  def test_get_registration_when_ok(self):
    self.db_insert_registration('hulot@mail.com', 'myToken')

    response = self.get_registration('myToken')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'result': {
        'registration': {
          'email': 'hulot@mail.com',
        },
      },
    })

  def test_get_registration_when_missing(self):
    response = self.get_registration('myToken')

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

  def test_post_registration_when_credentials_ok(self):
    self.db_insert_registration('hulot@mail.com', 'myToken')

    response = self.post_registration('myToken', 'myUsername', 'myPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertEqual(response.json, {
      'status': 'success',
      'message': 'Registration successful',
    })

  def test_post_registration_when_username_already_taken(self):
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')
    self.db_insert_registration('new@mail.com', 'token')

    response = self.post_registration('token', 'hulot', 'password')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'Username already taken',
    })

  def post_registration_email(self, email: str) -> Response:
    resource = '/authentication/registration'
    return self.client.post(resource, json={'email': email})

  def get_registration(self, token: str) -> Response:
    return self.client.get(f'/authentication/registration/{token}')

  def post_registration(self,
        token: str,
        username: str,
        password: str) -> Response:
    resource = f'/authentication/registration/{token}'
    json = {'username': username, 'password': password}
    return self.client.post(resource, json=json)


class TestPasswordUpdate(AppTestCase):

  def setUp(self) -> None:
    super().setUp()
    self.db_setup_account(1, 1, 'hulot', 'oldPassword', 'hulot@mail.com')
    self.token_factory = AuthenticationTokenFactory(
      self._app.secret_key, datetime.datetime.utcnow)

  def test_post_password_update_when_ok(self) -> None:
    token = self.get_authentication_token('hulot', 'oldPassword')

    response = self.post_password_update(token, 'oldPassword', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

  def test_post_password_update_when_token_missing(self) -> None:
    response = self.post_password_update(None, 'oldPassword', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'authentication token required',
    })

  def test_post_password_update_when_token_invalid(self) -> None:
    response = self.post_password_update('invalid', 'oldPassword',
                                         'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'authentication token invalid',
    })

  def test_post_password_update_when_token_expired(self) -> None:
    expiration = timedelta(seconds=-1)
    token = self.token_factory.create_authentication_token(1, expiration)

    response = self.post_password_update(token, 'oldPassword', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'authentication token expired',
    })

  def test_post_password_update_when_old_password_incorrect(self) -> None:
    token = self.get_authentication_token('hulot', 'oldPassword')

    response = self.post_password_update(token, 'incorrect', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'old password incorrect',
    })

  def test_post_password_update_when_new_password_invalid(self) -> None:
    token = self.get_authentication_token('hulot', 'oldPassword')

    response = self.post_password_update(token, 'oldPassword', 'invalid')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    self.assertEqual(response.json, {
      'status': 'failure',
      'message': 'new password invalid',
    })

  def post_password_update(self,
        token: Optional[str],
        old_password: str,
        new_password: str) -> Response:
    resource = '/authentication/password'
    headers = {'authToken': token} if token else {}
    json = {'oldPassword': old_password, 'newPassword': new_password}
    return self.client.post(resource, headers=headers, json=json)
