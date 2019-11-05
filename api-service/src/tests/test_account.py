from hashlib import pbkdf2_hmac
from unittest import TestCase
from unittest.mock import Mock, call, MagicMock
from types import SimpleNamespace as Simple
from binascii import hexlify

from birding.account import Account, PasswordRepository, PasswordResetToken, \
  PasswordHasher, TokenFactory, \
  AccountRepository, Username, Password, AccountFactory
from birding.account import Credentials
from birding.database import Database
from birding.database import read_script_file
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
    self.database = Mock(spec=Database)
    self.password_hasher = Mock(spec=PasswordHasher)
    self.token_factory = Mock(spec=TokenFactory)
    self.session = Mock()
    self.repository = AccountRepository(
      self.database,
      self.password_hasher,
      self.token_factory,
      self.session,
    )

  def test_find_account_by_id_queries_database_correctly(self) -> None:
    self.database.transaction.return_value = mock_database_transaction()
    self.database.transaction().execute.return_value = Simple(rows=[])

    self.repository.account_by_id(4)

    self.session.query.assert_called_with(Account)

  def test_create_account_registration_queries_database_correctly(self):
    email = EmailAddress('e@mail.com')
    token = self.token_factory.create_token()
    self.database.query.side_effect = [
      Simple(rows=[[4, 'e@mail.com', 'myToken']])]

    self.repository.create_account_registration(email)

    self.database.query.assert_has_calls([
      call(
        'INSERT INTO account_registration (email, token) '
        'VALUES (%s, %s) '
        'ON CONFLICT (email) DO UPDATE SET token = EXCLUDED.token '
        'RETURNING id, email, token;',
        (email.raw, token)),
    ])

  def test_find_account_registration_by_token_queries_database_correctly(self):
    self.database.query().rows = []
    self.repository.find_account_registration_by_token('myToken')
    self.database.query.assert_called_with(
      'SELECT id, email, token FROM account_registration WHERE token LIKE %s;',
      ('myToken',))


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


class TestPasswordRepository(TestCase):

  def setUp(self):
    self.token_factory = Mock()
    self.database = Mock()
    self.password_hasher = Mock()
    self.salt_factory = Mock()
    self.session = Mock()
    self.repository = PasswordRepository(
      self.token_factory,
      self.database,
      self.password_hasher,
      self.session,
    )

  def test_create_password_reset_token_queries_database_correctly(self):
    account = Simple(id=1)
    self.token_factory.create_token.return_value = 'myToken'
    self.database.query.side_effect = [
      Simple(status='INSERT'),
      Simple(rows=[[1, 'some token, hopefully the just inserted one']])
    ]

    self.repository.create_password_reset_token(account)

    insert_call = call(
      'INSERT INTO password_reset_token (account_id, token) VALUES (%s, %s) ON CONFLICT (account_id) DO UPDATE SET token = excluded.token;',
      (1, 'myToken'))
    select_call = call(
      'SELECT account_id, token FROM password_reset_token WHERE account_id = %s;',
      (account.id,))
    self.database.query.assert_has_calls([insert_call, select_call])

  def test_create_password_reset_token_returns_selected_token(self):
    account = Simple(id=1)
    self.database.query.side_effect = [
      Simple(status='INSERT'),
      Simple(rows=[[1, 'selectedToken']])
    ]

    result = self.repository.create_password_reset_token(account)

    self.assertEqual(result, PasswordResetToken(1, 'selectedToken'))

  def test_create_password_reset_token_replaces_previously_existing_token(self):
    account = Simple(id=1)
    self.database.query.side_effect = [
      Simple(status='INSERT'),
      Simple(rows=[[1, 'selectedToken']])
    ]

    result = self.repository.create_password_reset_token(account)

    self.assertEqual(result, PasswordResetToken(1, 'selectedToken'))

  def test_find_password_reset_token_queries_database_correctly(self):
    account = Simple(id=1)
    self.database.query.return_value = Simple(rows=[[1, 'token']])

    self.repository.find_password_reset_token(account)

    self.database.query.assert_called_with(
      'SELECT account_id, token FROM password_reset_token WHERE account_id = %s;',
      (account.id,))

  def test_find_password_reset_account_id_queries_database_correctly(self):
    self.database.query.return_value = Simple(rows=[])
    self.repository.find_password_reset_account_id('myToken')
    self.database.query.assert_called_with(
      'SELECT account_id FROM password_reset_token WHERE token LIKE %s;',
      ('myToken',))

  def test_find_password_reset_account_id_parses_response_correctly(self):
    self.database.query.return_value = Simple(rows=[[4]])
    result = self.repository.find_password_reset_account_id('myToken')
    self.assertEqual(result, 4)

  def test_update_password_queries_database_correctly(self):
    self.password_hasher.create_salt_hashed_password.return_value = (
      'mySalt', 'myHashedPassword')
    self.repository.update_password(4, 'myNewPassword')
    self.database.query.assert_called_with(
      'UPDATE hashed_password SET salt = %s, salted_hash = %s WHERE account_id = %s;',
      ('mySalt', 'myHashedPassword', 4))

  def test_remove_password_reset_token_queries_database_correctly(self):
    self.repository.remove_password_reset_token('myToken')
    self.database.query.assert_called_with(
      'DELETE FROM password_reset_token WHERE token LIKE %s;', ('myToken',))


class TestPasswordResetToken(TestCase):

  def test_repr(self):
    token = PasswordResetToken(4, 'token')
    self.assertEqual(repr(token), 'PasswordResetToken(4, token)')

  def test_eq_false_when_other_type(self):
    token = PasswordResetToken(4, 'token')
    self.assertNotEqual(token, 'PasswordResetToken(4, token)')
