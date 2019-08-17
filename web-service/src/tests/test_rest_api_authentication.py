import json
from http import HTTPStatus

from test_util import AppTestCase


class TestLogin(AppTestCase):

  def test_get_token_when_correct_credentials(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.db_insert_password(4, 'myPassword')

    response = self.get_authentication_token('myUsername', 'myPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    self.assertEqual(data['message'], 'Successfully logged in.')
    self.assertIn('authToken', data)

  def test_get_token_when_incorrect_credentials(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.db_insert_password(4, 'myPassword')

    response = self.get_authentication_token('somethingElse', 'notGood')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'Try again')
    self.assertNotIn('auth_token', data)

  def get_authentication_token(self, username, password):
    return self.client.get(
      f'/v2/authentication/token?username={username}&password={password}'
    )


class TestPasswordReset(AppTestCase):

  def test_post_password_reset_email_when_email_not_linked_with_account(self):
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'E-mail not associated with any account')

  def test_post_password_reset_email_when_email_associated_with_account(self):
    self.db_insert_person(1)
    self.db_insert_account(1, 'bolas', 'bolas@mail.com', 1, None)
    self.db_insert_locale(1, 'en')

    response = self.post_password_reset_email('bolas@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')
    self.assertEqual(data['message'], 'Password reset link sent to e-mail')

  def post_password_reset_email(self, email):
    json = {'email': email}
    return self.client.post('/v2/authentication/password-reset', json=json)


class TestRegister(AppTestCase):

  def test_post_registration_email_when_email_not_taken(self):
    self.db_insert_locale(1, 'en')

    response = self.post_registration_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'success')

  def test_post_registration_email_when_email_invalid(self):
    self.db_insert_locale(1, 'en')

    response = self.post_registration_email('hulot')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'Email invalid')

  def test_post_registration_email_when_email_taken(self):
    self.db_insert_locale(1, 'en')
    self.db_insert_person(1)
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', 1, None)

    response = self.post_registration_email('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
    data = json.loads(response.data.decode('utf-8'))
    self.assertEqual(data['status'], 'failure')
    self.assertEqual(data['message'], 'Email taken')

  def post_registration_email(self, email):
    return self.client.post(
      '/v2/authentication/registration',
      json={'email': email})
