import datetime
from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple
from birding.authentication import AccountRegistrationController
from birding.authentication import AuthenticationTokenFactory
from birding.authentication import AuthenticationTokenDecoder
from birding.authentication import PasswordResetController
from birding.account import AccountRepository, Username, Password, \
  AccountFactory
from birding.person import PersonRepository
from birding.mail import MailServerDispatcher
from birding.mail import EmailAddress
from birding.link import LinkFactory
from tests.test_util import mock_return

valid_email = 'valid@email.com'
valid_username = 'myUsername'
valid_password = 'myPassword'


class TestAccountRegistrationController(TestCase):

  def setUp(self):
    self.account_factory = Mock(spec=AccountFactory)
    self.account_repository = Mock(spec=AccountRepository)
    self.mail_dispatcher = Mock(spec=MailServerDispatcher)
    self.link_factory = Mock(spec=LinkFactory)
    self.person_repository = Mock(spec=PersonRepository)
    self.controller = AccountRegistrationController(
        self.account_factory,
        self.account_repository,
        self.mail_dispatcher,
        self.link_factory,
        self.person_repository,
    )

  def test_initiate_registration_when_invalid_email(self) -> None:
    result = self.controller.initiate_registration('invalid@email', Mock())
    self.assertEqual(result, 'email invalid')

  def test_initiate_registration_when_invalid_but_taken_email(self):
    result = self.controller.initiate_registration('taken@gmail.com', Mock())
    self.assertEqual(result, 'email taken')

  def test_initiate_registration_creates_correct_registration_link_when_valid_email_and_rest_api(self):
    locale = Mock()
    locale.text.return_value='translated'
    self.account_repository.create_account_registration().token = 'myToken'
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.link_factory.create_frontend_link.assert_called_with(
      '/authentication/registration/myToken')

  def test_initiate_registration_dispatches_registration_link_when_valid_free_email(self):
    locale = Simple(text=mock_return('translated message: '))
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(EmailAddress(valid_email), 'Birding Registration', 'translated message: myLink')

  def test_initiate_registration_returns_registration_when_success(self):
    locale = Simple(text=mock_return('translated'))
    registration = self.account_repository.create_account_registration()
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.assertIs(result, registration)

  def test_perform_registration_associated_registration_missing(self):
    self.account_repository.find_account_registration = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken', valid_username, valid_password)
    self.assertEqual(result, 'associated registration missing')

  def test_perform_registration_username_taken(self):
    self.account_repository.find_user_account = mock_return('uh-oh!')
    result = self.controller.perform_registration(valid_email, 'myToken', valid_username, valid_password)
    self.account_repository.find_user_account.assert_called_with(Username(valid_username))
    self.assertEqual(result, 'username taken')

  def test_perform_registration_creates_account(self):
    self.account_repository.find_user_account.return_value = None
    self.controller.perform_registration(valid_email, 'myToken', valid_username, valid_password)
    self.account_factory.create_account.assert_called_with(EmailAddress(valid_email), Username(valid_username), Password(valid_password))

  def test_perform_registration_removes_registration_on_success(self):
    registration = self.account_repository.find_account_registration()
    self.account_repository.find_user_account = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken', valid_username, valid_password)
    self.account_repository.remove_account_registration_by_id.assert_called_with(registration.id)
    self.assertEqual(result, 'success')

  def test_perform_registration_initializes_account_person_on_success(self):
    account = self.account_factory.create_account()
    person = self.person_repository.add_person()
    self.account_repository.find_user_account = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken', valid_username, valid_password)
    self.person_repository.add_person.assert_called_with(account.username)
    self.account_repository.set_user_account_person.assert_called_with(account, person)
    self.assertEqual(result, 'success')

class TestPasswordResetController(TestCase):

  def setUp(self):
    self.account_repository = Mock()
    self.password_repository = Mock()
    self.link_factory = Mock()
    self.mail_dispatcher = Mock()
    self.controller = PasswordResetController(
        self.account_repository,
        self.password_repository,
        self.link_factory,
        self.mail_dispatcher,
    )

  def test_initiate_password_reset_creates_token_when_account_present(self):
    locale = Simple(text=mock_return('translated: '))
    account = Simple()
    self.link_factory.create_frontend_link = mock_return('myLink')
    self.account_repository.find_account_by_email = mock_return(account)

    self.controller.initiate_password_reset(valid_email, locale)

    self.account_repository.find_account_by_email.assert_called_with(EmailAddress(valid_email))
    self.password_repository.create_password_reset_token.assert_called_with(account)

  def test_initiate_password_reset_not_create_token_when_account_not_present(self):
    self.account_repository.find_account_by_email = mock_return(None)

    self.controller.initiate_password_reset(valid_email, None)

    self.account_repository.find_account_by_email.assert_called_with(EmailAddress(valid_email))
    self.password_repository.create_password_reset_token.assert_not_called()

  def test_initiate_password_reset_dispatches_email_with_link(self):
    locale = Simple(text=mock_return('translated: '))
    self.link_factory.create_frontend_link = mock_return('myLink')

    self.controller.initiate_password_reset(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(EmailAddress(valid_email), 'Birding Password Reset', 'translated: myLink')

  def test_initiate_password_reset_creates_correct_frontend_link(self):
    locale = Simple(text=mock_return('translated: '))
    password_reset_token = Simple(token='myToken')
    self.link_factory.create_frontend_link = mock_return('myLink')
    self.password_repository.create_password_reset_token = mock_return(password_reset_token)

    self.controller.initiate_password_reset(valid_email, locale)

    self.link_factory.create_frontend_link.assert_called_with('/authentication/password-reset/myToken')

  def test_perform_password_reset_updates_password_when_reset_token_present(self):
    token = 'myToken'
    self.password_repository.find_password_reset_account_id.return_value = 4

    result = self.controller.perform_password_reset(token, valid_password)

    self.password_repository.find_password_reset_account_id.assert_called_with(token)
    self.password_repository.update_password.assert_called_with(
      4, Password(valid_password))
    self.assertEqual(result, 'success')

  def test_perform_password_reset_removes_password_reset_token_on_success(self):
    result = self.controller.perform_password_reset('myToken', valid_password)
    self.password_repository.remove_password_reset_token.assert_called_with('myToken')

class TestAuthenticationTokenFactory(TestCase):

  def test_encode_token(self):
    utc_now_supplier = lambda : datetime.datetime(2019, 8, 3, 20, 31)
    factory = AuthenticationTokenFactory('secret', utc_now_supplier)

    token = factory.create_authentication_token(1)

    self.assertEqual(token, (
      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ4NjYwNjAsImlhdCI6MTU'
      '2NDg2NDI2MCwic3ViIjoxfQ.WSvE-OCzvVPVayHicY1viqLYYA560cCK-9FOZ6NY2o0'))

class TestAuthenticationTokenDecoder(TestCase):

  def test_decode_token(self):
    factory = AuthenticationTokenFactory('secret', datetime.datetime.utcnow)
    token = factory.create_authentication_token(1)
    decoder = AuthenticationTokenDecoder('secret')

    result = decoder.decode_authentication_token(token)

    self.assertTrue(result.ok)
    self.assertEqual(result.payload['sub'], 1)

  def test_decode_expired_token(self):
    utc_now_supplier = lambda: datetime.datetime(2008, 8, 3, 20, 31)
    factory = AuthenticationTokenFactory('secret', utc_now_supplier)
    token = factory.create_authentication_token(1)
    decoder = AuthenticationTokenDecoder('secret')

    result = decoder.decode_authentication_token(token)

    self.assertFalse(result.ok)
    self.assertEqual(result.error, 'signature-expired')

  def test_decode_invalid_token(self):
    decoder = AuthenticationTokenDecoder('secret')

    result = decoder.decode_authentication_token('asdfasf.dsafasd.asdfasdf')

    self.assertFalse(result.ok)
    self.assertEqual(result.error, 'token-invalid')
