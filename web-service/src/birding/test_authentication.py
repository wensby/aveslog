from unittest import TestCase
from unittest.mock import Mock
from .authentication import AccountRegistrationController
from .authentication import AccountRegistrationRequest
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
    self.controller = AccountRegistrationController(
        self.account_repository, self.mail_dispatcher, self.link_factory, 
        self.person_repository)

  def test_initiate_registration_none_when_invalid_email(self):
    result = self.controller.initiate_registration('invalid@email')
    self.assertIsNone(result)

  def test_initiate_registration_puts_user_account_registration_when_valid_email(self):
    self.link_factory.create_endpoint_external_link = mock_return('myRegistrationLink')
    result = self.controller.initiate_registration(valid_email)
    self.account_repository.put_user_account_registration.assert_called()

  def test_initiate_registration_creates_correct_registration_link_when_valid_email(self):
    token = 'myToken'
    self.account_repository.get_user_account_registration_by_email().token = token
    self.link_factory.create_endpoint_external_link = mock_return('myRegistrationLink')
    result = self.controller.initiate_registration(valid_email)
    self.link_factory.create_endpoint_external_link.assert_called_with('authentication.get_register_form', token=token)

  def test_initiate_registration_dispatches_registration_link_when_valid_email(self):
    link = 'myLink'
    self.link_factory.create_endpoint_external_link = mock_return(link)
    result = self.controller.initiate_registration(valid_email)
    self.mail_dispatcher.dispatch.assert_called_with(valid_email, 'Birding Registration', f'Link: {link}')

  def test_initiate_registration_returns_registration_when_success(self):
    registration = self.account_repository.get_user_account_registration_by_email()
    registration.email = valid_email
    self.link_factory.create_endpoint_external_link = mock_return('myLink')
    self.account_repository.get_user_account_registration_by_email = mock_return(registration)
    result = self.controller.initiate_registration(valid_email)
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
