from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple
from birding.authentication import AccountRegistrationController
from birding.authentication import AccessToken
from birding.authentication import PasswordUpdateController
from birding.authentication import JwtFactory
from birding.authentication import AuthenticationTokenFactory
from birding.authentication import JwtDecoder
from birding.authentication import PasswordResetController
from birding.authentication import Authenticator
from birding.authentication import PasswordHasher
from birding.authentication import RefreshToken
from birding.authentication import RefreshTokenRepository
from birding.account import Account, TokenFactory
from birding.account import PasswordRepository
from birding.account import Credentials
from birding.account import AccountRepository, Username, Password, \
  AccountFactory
from birding.birder import BirderRepository
from birding.mail import MailServerDispatcher
from birding.mail import EmailAddress
from birding.link import LinkFactory
from tests.test_util import mock_return

valid_email = 'valid@email.com'
valid_username = 'myUsername'
valid_password = 'myPassword'


class TestAccessToken(TestCase):

  def test_eq_when_other_type(self):
    access_token = AccessToken('jwt', 1, datetime(2019, 10, 13))
    self.assertNotEqual(access_token, 'AccessToken(jwt, 1, 2019-10-13)')

  def test_hash(self):
    access_token = AccessToken('jwt', 1, datetime(2019, 10, 13))
    self.assertIsInstance(hash(access_token), int)

  def test_repr(self):
    access_token = AccessToken('jwt', 1, datetime(2019, 10, 13))
    token_repr = repr(access_token)
    self.assertEqual(token_repr, 'AccessToken(jwt, 1, 2019-10-13 00:00:00)')


class TestAuthenticator(TestCase):

  def setUp(self) -> None:
    self.account_repository = Mock(spec=AccountRepository)
    self.password_hasher = Mock(spec=PasswordHasher)

  def test_is_password_incorrect_when_hashed_password_missing(self) -> None:
    account = Account()
    authenticator = Authenticator(self.account_repository, self.password_hasher)
    self.account_repository.find_hashed_password.return_value = None

    result = authenticator.is_account_password_correct(account, 'idontexist')

    self.assertFalse(result)


class TestAccountRegistrationController(TestCase):

  def setUp(self):
    self.account_factory = Mock(spec=AccountFactory)
    self.account_repository = Mock(spec=AccountRepository)
    self.mail_dispatcher = Mock(spec=MailServerDispatcher)
    self.link_factory = Mock(spec=LinkFactory)
    self.birder_repository = Mock(spec=BirderRepository)
    self.token_factory = Mock(spec=TokenFactory)
    self.controller = AccountRegistrationController(
      self.account_factory,
      self.account_repository,
      self.mail_dispatcher,
      self.link_factory,
      self.birder_repository,
      self.token_factory
    )

  def test_initiate_registration_when_invalid_email(self) -> None:
    result = self.controller.initiate_registration('invalid@email', Mock())
    self.assertEqual(result, 'email invalid')

  def test_initiate_registration_when_invalid_but_taken_email(self):
    result = self.controller.initiate_registration('taken@gmail.com', Mock())
    self.assertEqual(result, 'email taken')

  def test_initiate_registration_creates_correct_registration_link_when_valid_email_and_rest_api(
        self):
    locale = Mock()
    locale.text.return_value = 'translated'
    self.account_repository.add_account_registration().token = 'myToken'
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.link_factory.create_frontend_link.assert_called_with(
      '/authentication/registration/myToken')

  def test_initiate_registration_dispatches_registration_link_when_valid_free_email(
        self):
    locale = Mock()
    locale.text.return_value = 'translated message: '
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(EmailAddress(valid_email),
                                                     'Birding Registration',
                                                     'translated message: myLink')

  def test_initiate_registration_returns_registration_when_success(self):
    locale = Mock()
    locale.text.return_value = 'translated'
    registration = self.account_repository.add_account_registration()
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.assertIs(result, registration)

  def test_perform_registration_associated_registration_missing(self):
    self.account_repository.find_account_registration = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken',
                                                  valid_username,
                                                  valid_password)
    self.assertEqual(result, 'associated registration missing')

  def test_perform_registration_username_taken(self):
    self.account_repository.find_account = mock_return('uh-oh!')
    result = self.controller.perform_registration(valid_email, 'myToken',
                                                  valid_username,
                                                  valid_password)
    self.account_repository.find_account.assert_called_with(
      Username(valid_username))
    self.assertEqual(result, 'username taken')

  def test_perform_registration_creates_account(self):
    self.account_repository.find_account.return_value = None
    self.controller.perform_registration(valid_email, 'myToken', valid_username,
                                         valid_password)
    self.account_factory.create_account.assert_called_with(
      EmailAddress(valid_email), Credentials(Username(valid_username),
                                             Password(valid_password)))

  def test_perform_registration_removes_registration_on_success(self):
    registration = self.account_repository.find_account_registration()
    self.account_repository.find_account = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken',
                                                  valid_username,
                                                  valid_password)
    self.account_repository.remove_account_registration_by_id.assert_called_with(
      registration.id)
    self.assertEqual(result, 'success')

  def test_perform_registration_initializes_account_birder_on_success(self):
    account = self.account_factory.create_account()
    birder = self.birder_repository.add_birder()
    self.account_repository.find_account = mock_return(None)
    result = self.controller.perform_registration(valid_email, 'myToken',
                                                  valid_username,
                                                  valid_password)
    self.birder_repository.add_birder.assert_called_with(account.username)
    self.account_repository.set_account_birder.assert_called_with(account,
                                                                  birder)
    self.assertEqual(result, 'success')


class TestPasswordResetController(TestCase):

  def setUp(self):
    self.account_repository: AccountRepository = Mock(spec=AccountRepository)
    self.password_repository = Mock()
    self.link_factory = Mock()
    self.mail_dispatcher = Mock()
    self.password_update_controller: PasswordUpdateController = Mock(
      spec=PasswordUpdateController)
    self.refresh_token_repository: RefreshTokenRepository = Mock(
      spec=RefreshTokenRepository)
    self.token_factory = Mock()
    self.controller = PasswordResetController(
      self.account_repository,
      self.password_repository,
      self.link_factory,
      self.mail_dispatcher,
      self.password_update_controller,
      self.token_factory,
    )

  def test_initiate_password_reset_creates_token_when_account_present(self):
    locale = Mock()
    locale.text.return_value = 'translated: '
    account = Account(id=4)
    self.link_factory.create_frontend_link = mock_return('myLink')
    self.account_repository.find_account_by_email = mock_return(account)

    self.controller.initiate_password_reset(valid_email, locale)

    self.account_repository.find_account_by_email.assert_called_with(
      EmailAddress(valid_email))
    self.password_repository.add_password_reset_token.assert_called()

  def test_initiate_password_reset_not_create_token_when_account_not_present(
        self):
    self.account_repository.find_account_by_email = mock_return(None)

    self.controller.initiate_password_reset(valid_email, Mock())

    self.account_repository.find_account_by_email.assert_called_with(
      EmailAddress(valid_email))
    self.password_repository.add_password_reset_token.assert_not_called()

  def test_initiate_password_reset_dispatches_email_with_link(self):
    locale = Mock()
    locale.text.return_value = 'translated: '
    self.link_factory.create_frontend_link = mock_return('myLink')

    self.controller.initiate_password_reset(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(EmailAddress(valid_email),
                                                     'Birding Password Reset',
                                                     'translated: myLink')

  def test_initiate_password_reset_creates_correct_frontend_link(self):
    locale = Mock()
    locale.text.return_value = 'translated: '
    self.token_factory.create_token.return_value = 'myToken'
    self.link_factory.create_frontend_link = mock_return('myLink')

    self.controller.initiate_password_reset(valid_email, locale)

    self.link_factory.create_frontend_link.assert_called_with(
      '/authentication/password-reset/myToken')

  def test_perform_password_reset_updates_password_when_reset_token_present(
        self):
    token = 'myToken'
    self.password_repository.find_password_reset_token_by_token.return_value = Simple(
      account_id=4)
    account = Account()
    self.account_repository.account_by_id.return_value = account

    result = self.controller.perform_password_reset(token, valid_password)

    self.password_repository.find_password_reset_token_by_token.assert_called_with(
      token)
    self.assertEqual(result, 'success')
    self.password_update_controller.update_password.assert_called_with(
      account, Password(valid_password))

  def test_perform_password_reset_removes_password_reset_token_on_success(self):
    result = self.controller.perform_password_reset('myToken', valid_password)
    self.password_repository.remove_password_reset_token.assert_called_with(
      'myToken')


class TestAuthenticationTokenFactory(TestCase):

  def test_encode_token(self):
    utc_now_supplier = lambda: datetime(2019, 8, 3, 20, 31)
    jwt_factory = JwtFactory('secret')
    factory = AuthenticationTokenFactory(jwt_factory, utc_now_supplier)

    token = factory.create_access_token(1)

    self.assertEqual(
      token, AccessToken(
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ4NjYwNjAsImlhdCI6M'
        'TU2NDg2NDI2MCwic3ViIjoxfQ.WSvE-OCzvVPVayHicY1viqLYYA560cCK-9FOZ6NY2o0',
        1, datetime(2019, 8, 3, 21, 1)))


class TestJwtDecoder(TestCase):

  def test_decode_jwt(self):
    jwt_factory = JwtFactory('secret')
    factory = AuthenticationTokenFactory(jwt_factory, datetime.utcnow)
    token = factory.create_access_token(1)
    decoder = JwtDecoder('secret')

    result = decoder.decode_jwt(token.jwt)

    self.assertTrue(result.ok)
    self.assertEqual(result.payload['sub'], 1)

  def test_decode_expired_jwt(self):
    utc_now_supplier = lambda: datetime(2008, 8, 3, 20, 31)
    jwt_factory = JwtFactory('secret')
    factory = AuthenticationTokenFactory(jwt_factory, utc_now_supplier)
    token = factory.create_access_token(1)
    decoder = JwtDecoder('secret')

    result = decoder.decode_jwt(token.jwt)

    self.assertFalse(result.ok)
    self.assertEqual(result.error, 'signature-expired')

  def test_decode_invalid_jwt(self):
    decoder = JwtDecoder('secret')

    result = decoder.decode_jwt('asdfasf.dsafasd.asdfasdf')

    self.assertFalse(result.ok)
    self.assertEqual(result.error, 'token-invalid')


class TestRefreshToken(TestCase):

  def test_init(self):
    RefreshToken(
      id=1, token='jwt', account_id=1,
      expiration_date=datetime(2019, 10, 8, 12, 28, 0))

  def test_eq_when_identical(self):
    a = RefreshToken(id=1, token='jwt', account_id=1,
                     expiration_date=datetime(2019, 10, 8, 12, 28, 0))
    b = RefreshToken(id=1, token='jwt', account_id=1,
                     expiration_date=datetime(2019, 10, 8, 12, 28, 0))
    self.assertEqual(a, b)

  def test_eq_when_other_type(self):
    token = RefreshToken(id=1, token='jwt', account_id=1,
                         expiration_date=datetime(2019, 10, 8, 20, 46))
    self.assertNotEqual(token, 'RefreshToken(1, jwt, 1, 2019-10-08 20:46)')


class TestPasswordUpdateController(TestCase):

  def setUp(self) -> None:
    self.password_repository: PasswordRepository = Mock(
      spec=PasswordRepository)
    self.refresh_token_repository: RefreshTokenRepository = Mock(
      spec=RefreshTokenRepository)

  def test_invokes_correct_methods(self):
    account = Account(id=1)
    password = Password('costanza')
    controller = PasswordUpdateController(
      self.password_repository, self.refresh_token_repository)

    controller.update_password(account, password)

    self.password_repository.update_password.assert_called_with(1, password)
    self.refresh_token_repository.remove_refresh_tokens.assert_called_with(
      account)
