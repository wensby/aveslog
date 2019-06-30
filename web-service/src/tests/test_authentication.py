from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple
from birding.authentication import AccountRegistrationController
from birding.authentication import PasswordResetController
from birding.authentication import Authenticator
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

class TestAuthenticator(TestCase):

  def setUp(self):
    self.account_repository = Mock()
    self.password_hasher = Mock()
    self.authenticator = Authenticator(
        self.account_repository, 
        self.password_hasher,
    )

  def test_get_authenticated_user_account_when_correct_password(self):
    credentials = Mock()
    account = self.account_repository.find_user_account()
    hashed_password = self.account_repository.find_hashed_password()
    hashed_password.salted_hash = self.password_hasher.hash_password()

    result = self.authenticator.get_authenticated_user_account(credentials)

    self.account_repository.find_user_account.assert_called_with(credentials.username)
    self.assertEqual(result, account)

  def test_get_authenticated_user_account_none_when_wrong_password(self):
    self.password_hasher.hash_password.return_value = 'wrong_hash'
    result = self.authenticator.get_authenticated_user_account(Mock())
    self.assertIsNone(result)


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

  def test_initiate_registration_when_invalid_email(self):
    result = self.controller.initiate_registration('invalid@email', None)
    self.assertEqual(result, 'email invalid')

  def test_initiate_registration_when_invalid_but_taken_email(self):
    result = self.controller.initiate_registration('taken@gmail.com', None)
    self.assertEqual(result, 'email taken')

  def test_initiate_registration_creates_registration_when_valid_email(self):
    locale = Simple(text=mock_return('translated'))
    self.link_factory.create_endpoint_external_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.account_repository.create_account_registration.assert_called_with(EmailAddress(valid_email))

  def test_initiate_registration_creates_correct_registration_link_when_valid_email(self):
    locale = Simple(text=mock_return('translated'))
    self.account_repository.create_account_registration().token = 'myToken'
    self.link_factory.create_endpoint_external_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.link_factory.create_endpoint_external_link.assert_called_with('authentication.get_register_form', token='myToken')

  def test_initiate_registration_dispatches_registration_link_when_valid_free_email(self):
    locale = Simple(text=mock_return('translated message: '))
    self.link_factory.create_endpoint_external_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(EmailAddress(valid_email), 'Birding Registration', 'translated message: myLink')

  def test_initiate_registration_returns_registration_when_success(self):
    locale = Simple(text=mock_return('translated'))
    registration = self.account_repository.create_account_registration()
    self.link_factory.create_endpoint_external_link.return_value = 'myLink'
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

  def test_person_registration_request_failure_when_account_creation_fails(self):
    self.account_repository.find_user_account = mock_return(None)
    self.account_factory.create_account = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken', valid_username, valid_password)
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

    self.account_repository.find_account_by_email.assert_called_with(EmailAddress(valid_email))
    self.password_repository.create_password_reset_token.assert_called_with(account)

  def test_initiate_password_reset_not_create_token_when_account_not_present(self):
    self.account_repository.find_account_by_email = mock_return(None)

    self.controller.initiate_password_reset(valid_email, None)

    self.account_repository.find_account_by_email.assert_called_with(EmailAddress(valid_email))
    self.password_repository.create_password_reset_token.assert_not_called()

  def test_initiate_password_reset_dispatches_email_with_link(self):
    locale = Simple(text=mock_return('translated: '))
    self.link_factory.create_endpoint_external_link = mock_return('myLink')

    self.controller.initiate_password_reset(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(EmailAddress(valid_email), 'Birding Password Reset', 'translated: myLink')

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
