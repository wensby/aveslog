from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from aveslog.test_util import get_test_database_session
from aveslog.v0.authentication import AccountRegistrationController
from aveslog.v0.authentication import PasswordUpdateController
from aveslog.v0.authentication import AccessToken
from aveslog.v0.authentication import JwtFactory
from aveslog.v0.authentication import AuthenticationTokenFactory
from aveslog.v0.authentication import JwtDecoder
from aveslog.v0.authentication import Authenticator
from aveslog.v0.authentication import PasswordHasher
from aveslog.v0.account import TokenFactory
from aveslog.v0.models import Account, RefreshToken, HashedPassword, Base
from aveslog.v0.account import AccountRepository
from aveslog.mail import MailServerDispatcher
from aveslog.v0.link import LinkFactory

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
    self.password_hasher = Mock(spec=PasswordHasher)

  def test_is_password_incorrect_when_hashed_password_missing(self) -> None:
    authenticator = Authenticator(self.password_hasher)
    result = authenticator.is_account_password_correct(Account(), 'idontexist')
    self.assertFalse(result)


class TestAccountRegistrationController(TestCase):

  def setUp(self):
    self.account_repository = Mock(spec=AccountRepository)
    self.mail_dispatcher = Mock(spec=MailServerDispatcher)
    self.link_factory = Mock(spec=LinkFactory)
    self.token_factory = Mock(spec=TokenFactory)
    self.controller = AccountRegistrationController(
      self.account_repository,
      self.mail_dispatcher,
      self.link_factory,
      self.token_factory,
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
    locale.text.side_effect = ['translated-subject', 'translated message: ']
    self.account_repository.add_account_registration().token = 'myToken'
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.link_factory.create_frontend_link.assert_called_with(
      '/authentication/registration/myToken')

  def test_initiate_registration_dispatches_registration_link_when_valid_free_email(
        self):
    locale = Mock()
    locale.text.side_effect = ['translated-subject', 'translated message: ']
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.mail_dispatcher.dispatch.assert_called_with(valid_email,
      'translated-subject',
      'translated message: myLink')

  def test_initiate_registration_returns_registration_when_success(self):
    locale = Mock()
    locale.text.side_effect = ['translated-subject', 'translated message: ']
    registration = self.account_repository.add_account_registration()
    self.link_factory.create_frontend_link.return_value = 'myLink'
    self.account_repository.find_account_by_email.return_value = None

    result = self.controller.initiate_registration(valid_email, locale)

    self.assertIs(result, registration)


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


class TestPasswordUpdateController(TestCase):

  def setUp(self) -> None:
    self.db_session = get_test_database_session()
    self.password_hasher = Mock(spec=PasswordHasher)
    self.controller = PasswordUpdateController(self.password_hasher)

  def test_update_password_when_ok(self):
    account = Account(username='kennybostick', email='kenny.bostick@mail.com')
    password = HashedPassword(salt='salt1', salted_hash='salted_hash1')
    utcnow = datetime.utcnow()
    refresh_token = RefreshToken(token='token', expiration_date=utcnow)
    account.refresh_tokens.append(refresh_token)
    account.hashed_password = password
    self.db_session.add(account)
    self.db_session.flush()
    self.password_hasher.create_salt_hashed_password.return_value = (
      'salt2', 'salted_hash2')

    self.controller.update_password(account, 'birder-no-1', self.db_session)

    self.password_hasher.create_salt_hashed_password.assert_called_with(
      'birder-no-1')
    self.db_session.refresh(account)
    self.assertFalse(account.refresh_tokens)
    self.assertEqual(account.hashed_password.salt, 'salt2')
    self.assertEqual(account.hashed_password.salted_hash, 'salted_hash2')

  def tearDown(self):
    self.db_session.rollback()
    self.db_session.close()
