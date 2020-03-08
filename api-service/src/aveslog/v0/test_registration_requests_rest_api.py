from http import HTTPStatus

from flask import Response

from aveslog.test_util import AppTestCase
from aveslog.v0 import ErrorCode


class TestCreateRegistrationRequest(AppTestCase):

  def test_post_registration_request_when_ok(self):
    self.db_insert_locale(1, 'en')

    response = self.post_registration_request('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    self.assertIsNone(response.json)
    registration_requests = self.db_get_registration_requests()
    self.assertEqual(len(registration_requests), 1)
    token = registration_requests[0][2]
    self.assertEqual(len(self.dispatched_mails), 1)
    dispatched_mail = self.dispatched_mails[0]
    self.assertDictEqual(dispatched_mail, {
      'body':
        'Hi there, thanks for showing interest in aveslog. Here is your link '
        'to the registration form: '
        f'{self._app.config["FRONTEND_HOST"]}/authentication/registration/{token}',
      'recipient': 'hulot@mail.com',
      'subject': 'Birding Registration',
    })

  def test_post_registration_request_when_email_invalid(self):
    self.db_insert_locale(1, 'en')

    response = self.post_registration_request('hulot')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertDictEqual(response.json, {
      'code': ErrorCode.EMAIL_INVALID,
      'message': 'Email invalid',
    })
    self.assertListEqual(self.dispatched_mails, [])

  def test_post_registration_request_when_email_taken(self):
    self.db_insert_locale(1, 'en')
    self.db_setup_account(1, 1, 'hulot', 'myPassword', 'hulot@mail.com')

    response = self.post_registration_request('hulot@mail.com')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertDictEqual(response.json, {
      'code': ErrorCode.EMAIL_TAKEN,
      'message': 'Email taken',
    })

  def post_registration_request(self, email: str) -> Response:
    resource = '/registration-requests'
    return self.client.post(resource, json={'email': email})


class TestGetRegistrationRequest(AppTestCase):

  def test_get_registration_request_when_ok(self):
    self.db_insert_registration('hulot@mail.com', 'myToken')

    response = self.get_registration_request('myToken')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'token': 'myToken',
      'email': 'hulot@mail.com',
    })

  def test_get_registration_request_when_missing(self):
    response = self.get_registration_request('myToken')

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    self.assertIsNone(response.json)

  def get_registration_request(self, token: str) -> Response:
    return self.client.get(f'/registration-requests/{token}')
