from hashlib import pbkdf2_hmac
from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple
from binascii import hexlify

from birding.account import Account, PasswordRepository, PasswordResetToken, \
  PasswordHasher, TokenFactory, \
  AccountRepository, Username, Password, AccountFactory, AccountRegistration
from birding.account import Credentials
from birding.database import Database
from birding.mail import EmailAddress

from test_util import mock_database_transaction


class TestUsername(TestCase):

  def test_construction_throws_exception_when_invalid_format(self):
    self.assertRaises(Exception, Username, '')
    self.assertRaises(Exception, Username, '1234')
    self.assertRaises(Exception, Username, 'abcde@')
    self.assertRaises(Exception, Username, (''.join(['a'] * 33)))

  def test_eq_false_when_another_type(self):
    self.assertNotEqual(Username('hulot'), 'hulot')

  def test_repr(self):
    self.assertEqual(repr(Username('hulot')), 'Username(hulot)')


class TestPassword(TestCase):

  def test_construction_throws_exception_when_invalid_format(self):
    self.assertRaises(Exception, Password, '')
    self.assertRaises(Exception, Password, '1234567')
    self.assertRaises(Exception, Password, ('').join(['a'] * 129))

  def test_eq_false_when_another_type(self):
    self.assertNotEqual(Password('12345678'), '12345678')


class TestCredentials(TestCase):

  def test_eq_with_other_type(self) -> None:
    username = Username('kenny')
    password = Password('bostick!')
    credentials = Credentials(username, password)

    self.assertNotEqual(credentials, {
      'username': username, 'password': password
    })


class TestAccount(TestCase):

  @classmethod
  def setUpClass(cls) -> None:
    cls.account = Account(id=4, username='hulot', email='hulot@mail.com',
                          birder_id=8, locale_id=15)

  def test_eq_false_when_another_type(self):
    string_account = 'Account(4, hulot, hulot@email.com, 8, 15)'
    self.assertNotEqual(self.account, string_account)

  def test_repr(self):
    representation = repr(self.account)
    self.assertEqual(
      representation,
      "<Account(username='hulot', email='hulot@mail.com', "
      "birder_id='8', locale_id='15')>")


class TestAccountRepository(TestCase):

  def setUp(self):
    self.password_hasher = Mock(spec=PasswordHasher)
    self.token_factory = Mock(spec=TokenFactory)
    self.session = Mock()
    self.repository = AccountRepository(self.password_hasher, self.session)

  def test_find_account_by_id_queries_database_correctly(self) -> None:
    self.repository.account_by_id(4)
    self.session.query.assert_called_with(Account)

  def test_create_account_registration_queries_database_correctly(self):
    email = EmailAddress('e@mail.com')
    token = self.token_factory.create_token()
    account_registration = AccountRegistration(email=email.raw, token=token)

    self.repository.add_account_registration(account_registration)

    self.session.add.assert_called_with(account_registration)

  def test_find_account_registration_by_token_queries_database_correctly(self):
    self.repository.find_account_registration_by_token('myToken')
    self.session.query.assert_called_with(AccountRegistration)


class TestAccountFactory(TestCase):
  username = Username('alice')
  email = EmailAddress('alice@email.com')
  password = Password('password')
  credentials = Credentials(username, password)

  def setUp(self) -> None:
    self.database = Mock()
    self.password_hasher = Mock()
    self.account_repository: AccountRepository = Mock(spec=AccountRepository)
    self.password_repository = Mock()
    self.factory = AccountFactory(
      self.password_hasher,
      self.account_repository, self.password_repository)

  def test_create_account_returns_account_when_success(self):
    added_account = Account(
      id=4, username='alice', email='alice@email.com',
      birder_id=None, locale_id=None)
    self.password_hasher.create_salt_hashed_password.return_value = (
      'mySalt', 'mySaltedHash')
    self.account_repository.find_account.return_value = None
    self.account_repository.add.return_value = added_account

    result = self.factory.create_account(self.email, self.credentials)

    self.assertEqual(result, added_account)

  def test_create_account_fails_when_username_already_taken(self):
    self.database.transaction.return_value = mock_database_transaction()
    self.database.transaction().execute.return_value = Simple(rows=[[1]])

    result = self.factory.create_account(self.email, self.credentials)

    self.assertIsNone(result)

  def test_create_account_fails_when_inserting_account_fails(self):
    self.database.transaction.return_value = mock_database_transaction()
    self.database.transaction().execute.side_effect = [
      Simple(rows=[]),
      Simple(rows=[])]

    result = self.factory.create_account(self.email, self.credentials)

    self.assertIsNone(result)


class TestPasswordHasher(TestCase):

  def setUp(self):
    self.salt_factory = Mock()
    self.password_hasher = PasswordHasher(self.salt_factory)

  def test_create_salt_hashed_password_returns_salt_from_salt_factory(self):
    salt = 'mySalt'
    password = 'myPassword'
    self.salt_factory.create_salt.return_value = salt

    result = self.password_hasher.create_salt_hashed_password(
      Password(password))

    expected_hashed_password = hexlify(
      pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)).decode()
    self.assertEqual(result, (salt, expected_hashed_password))

  def test_hash_password(self):
    hasher = PasswordHasher(Mock())
    hash = '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
    self.assertTrue(hasher.hash_password(Password('password'), 'salt') == hash)


class TestPasswordResetToken(TestCase):

  def test_repr(self):
    token = PasswordResetToken(account_id=4, token='token')
    self.assertEqual(repr(token),
                     "<PasswordResetToken(account_id='4', token='token')>")

  def test_eq_false_when_other_type(self):
    token = PasswordResetToken(account_id=4, token='token')
    self.assertNotEqual(token, 'PasswordResetToken(4, token)')
