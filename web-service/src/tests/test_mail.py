import os
from unittest import TestCase

import birding
from birding.mail import EmailAddress, MailServerDispatcher


class TestEmailAddress(TestCase):

  def test_construction_when_invalid_format(self):
    self.assertRaises(Exception, EmailAddress, *('invalidformat',))

  def test_eq_false_when_different_type(self):
    self.assertNotEqual(EmailAddress('my@email.com'), 'my@email.com')

  def test_repr(self):
    self.assertEqual(
      repr(EmailAddress('my@mail.com')), 'EmailAddress<my@mail.com>')


class TestMailDispatcherFactory(TestCase):

  def setUp(self) -> None:
    os.environ['MAIL_SERVER'] = 'myMailServer'
    os.environ['MAIL_PORT'] = 'myMailPort'
    os.environ['MAIL_USERNAME'] = 'myMailUsername'
    os.environ['MAIL_PASSWORD'] = 'myMailPassword'
    os.environ['MAIL_USE_TLS'] = 'false'
    os.environ['MAIL_USE_SSL'] = 'true'

  def test_app_construction_with_mail_server_environment_variables(self):
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs'
    }
    birding.create_app(test_config=test_config)

  def tearDown(self) -> None:
    del os.environ['MAIL_SERVER']
    del os.environ['MAIL_PORT']
    del os.environ['MAIL_USERNAME']
    del os.environ['MAIL_PASSWORD']
    del os.environ['MAIL_USE_TLS']
    del os.environ['MAIL_USE_SSL']

class TestMailServerDispatcher(TestCase):

  def setUp(self) -> None:
    test_config = {
      'TESTING': True,
      'SECRET_KEY': 'wowsosecret',
      'LOGS_DIR_PATH': 'test-logs'
    }
    app = birding.create_app(test_config=test_config)
    self.dispatcher = MailServerDispatcher(app, None, None, 'myUsername', None, None, None)
    self.app_context = app.test_request_context()
    self.app_context.push()

  def test_dispatch(self):
    email_address = EmailAddress('my@email.com')
    self.dispatcher.dispatch(email_address, 'mySubject', 'myBody')

  def tearDown(self) -> None:
    self.app_context.pop()