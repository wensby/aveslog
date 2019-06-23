from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple
from .authentication import AccountRegistrationController
from .authentication import AccountRegistrationRequest
from .authentication import PasswordResetController
from .test_util import mock_return

valid_email = 'valid@email.com'
valid_username = 'myUsername'
valid_password = 'myPassword'

class TestAccountRegistrationController(TestCase):

  def setUp(self):
    self.account_repository = Mock()
    self.mail_dispatcher = Mock()
    self.link_factory = Mock()
    self.person_repository = Mock()
    self.locale = Mock()
    self.controller = AccountRegistrationController(
        self.account_repository, self.mail_dispatcher, self.link_factory, 
        self.person_repository)

  def test_initiate_registration_none_when_invalid_email(self):
    result = self.controller.initiate_registration('invalid@email', self.locale)
    self.assertIsNone(result)

  def test_initiate_registration_puts_user_account_registration_when_valid_email(self):
    self.locale.text = mock_return('translated')
    self.link_factory.create_endpoint_external_link = mock_return('myRegistrationLink')
    result = self.controller.initiate_registration(valid_email, self.locale)
    self.account_repository.put_user_account_registration.assert_called()

  def test_initiate_registration_creates_correct_registration_link_when_valid_email(self):
    self.locale.text = mock_return('translated')
    token = 'myToken'
    self.account_repository.get_user_account_registration_by_email().token = token
    self.link_factory.create_endpoint_external_link = mock_return('myRegistrationLink')
    result = self.controller.initiate_registration(valid_email, self.locale)
    self.link_factory.create_endpoint_external_link.assert_called_with('authentication.get_register_form', token=token)

  def test_initiate_registration_dispatches_registration_link_when_valid_email(self):
    self.locale.text = mock_return('translated message: ')
    link = 'myLink'
    self.link_factory.create_endpoint_external_link = mock_return(link)
    result = self.controller.initiate_registration(valid_email, self.locale)
    self.mail_dispatcher.dispatch.assert_called_with(valid_email, 'Birding Registration', f'translated message: {link}')

  def test_initiate_registration_returns_registration_when_success(self):
    self.locale.text = mock_return('translated')
    registration = self.account_repository.get_user_account_registration_by_email()
    registration.email = valid_email
    self.link_factory.create_endpoint_external_link = mock_return('myLink')
    self.account_repository.get_user_account_registration_by_email = mock_return(registration)
    result = self.controller.initiate_registration(valid_email, self.locale)
    self.assertIs(result, registration)

  def test_perform_registration_request_associated_registration_missing(self):
    request = AccountRegistrationRequest(valid_email, 'myToken', valid_username, valid_password)
    self.account_repository.find_account_registration = mock_return(None)
    result = self.controller.perform_registration_request(request)
    self.assertEqual(result, 'associated registration missing')

  def test_perform_registration_request_username_taken(self):
    request = AccountRegistrationRequest(valid_email, 'myToken', valid_username, valid_password)
    self.account_repository.find_user_account = mock_return('uh-oh!')
    result = self.controller.perform_registration_request(request)
    self.account_repository.find_user_account.assert_called_with(valid_username)
    self.assertEqual(result, 'username taken')

  def test_perform_registration_request_creates_account(self):
    request = AccountRegistrationRequest(valid_email, 'myToken', valid_username, valid_password)
    self.account_repository.find_user_account = mock_return(None)
    result = self.controller.perform_registration_request(request)
    self.account_repository.put_new_user_account.assert_called_with(valid_email, valid_username, valid_password)

  def test_perform_registration_request_removes_registration_on_success(self):
    request = AccountRegistrationRequest(valid_email, 'myToken', valid_username, valid_password)
    registration = self.account_repository.find_account_registration()
    self.account_repository.find_user_account = mock_return(None)
    result = self.controller.perform_registration_request(request)
    self.account_repository.remove_account_registration_by_id.assert_called_with(registration.id)
    self.assertEqual(result, 'success')

  def test_perform_registration_request_initializes_account_person_on_success(self):
    request = AccountRegistrationRequest(valid_email, 'myToken', valid_username, valid_password)
    account = self.account_repository.put_new_user_account()
    person = self.person_repository.add_person()
    self.account_repository.find_user_account = mock_return(None)
    result = self.controller.perform_registration_request(request)
    self.person_repository.add_person.assert_called_with(account.username)
    self.account_repository.set_user_account_person.assert_called_with(account, person)
    self.assertEqual(result, 'success')

  def test_person_registration_request_failure_when_account_creation_fails(self):
    request = AccountRegistrationRequest(valid_email, 'myToken', valid_username, valid_password)
    self.account_repository.find_user_account = mock_return(None)
    self.account_repository.put_new_user_account = mock_return(None)
    result = self.controller.perform_registration_request(request)
    self.assertEqual(result, 'failure')

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
    self.link_factory.create_endpoint_external_link = mock_return('myLink')
    self.account_repository.find_account_by_email = mock_return(account)

    self.controller.initiate_password_reset(valid_email, locale)

    self.account_repository.find_account_by_email.assert_called_with(valid_email)
    self.password_repository.create_password_reset_token.assert_called_with(account)

  def test_initiate_password_reset_not_create_token_when_account_not_present(self):
    self.account_repository.find_account_by_email = mock_return(None)

    self.controller.initiate_password_reset(valid_email, None)

    self.account_repository.find_account_by_email.assert_called_with(valid_email)
    self.password_repository.create_password_reset_token.assert_not_called()

  def test_initiate_password_reset_dispatches_email_with_link(self):
    locale = Simple(text=mock_return('translated: '))
    self.link_factory.create_endpoint_external_link = mock_return('myLink')

    self.controller.initiate_password_reset(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(valid_email, 'Birding Password Reset', 'translated: myLink')

  def test_initiate_password_reset_creates_link_for_correct_endpoint(self):
    locale = Simple(text=mock_return('translated: '))
    password_reset_token = Simple(token='myToken')
    self.link_factory.create_endpoint_external_link = mock_return('myLink')
    self.password_repository.create_password_reset_token = mock_return(password_reset_token)

    self.controller.initiate_password_reset(valid_email, locale)

    self.link_factory.create_endpoint_external_link.assert_called_with('authentication.get_password_reset_form', token='myToken')

  def test_perform_password_reset_updates_password_when_reset_token_present(self):
    token = 'myToken'
    self.password_repository.find_password_reset_account_id.return_value = 4

    result = self.controller.perform_password_reset(token, valid_password)

    self.password_repository.find_password_reset_account_id.assert_called_with(token)
    self.password_repository.update_password.assert_called_with(4, valid_password)
    self.assertEqual(result, 'success')

  def test_perform_password_reset_removes_password_reset_token_on_success(self):
    result = self.controller.perform_password_reset('myToken', valid_password)
    self.password_repository.remove_password_reset_token.assert_called_with('myToken')
