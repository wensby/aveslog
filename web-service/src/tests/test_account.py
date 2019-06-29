import unittest
from hashlib import pbkdf2_hmac
from unittest import TestCase
from unittest.mock import Mock, call
from types import SimpleNamespace as Simple
from binascii import hexlify

from birding.account import Account, PasswordRepository, PasswordResetToken, PasswordHasher, TokenFactory, \
  AccountRepository
from birding.database import Database
from birding.mail import EmailAddress

class TestAccountRepository(TestCase):

  def setUp(self):
    self.database = Mock(spec=Database)
    self.password_hasher = Mock(spec=PasswordHasher)
    self.token_factory = Mock(spec=TokenFactory)
    self.repository = AccountRepository(
        self.database, 
        self.password_hasher,
        self.token_factory,
    )

  def test_find_account_by_id_queries_database_correctly(self):
    self.database.query().rows = []
    result = self.repository.find_account_by_id(4)
    self.database.query.assert_called_with('SELECT id, username, email, person_id, locale_id FROM user_account WHERE id = %s;', (4,))

  def test_find_account_by_id_parses_account_correctly_when_present(self):
    self.database.query().rows = [[4, 'username', 'e@mail.com', 8, 15]]
    result = self.repository.find_account_by_id(4)
    self.assertEqual(result, Account(4, 'username', 'e@mail.com', 8, 15))

  def test_create_account_registration_queries_database_correctly(self):
    email = EmailAddress('e@mail.com')
    token = self.token_factory.create_token()
    self.database.query.side_effect = [Simple(rows=[[4, 'e@mail.com', 'myToken']])]

    self.repository.create_account_registration(email)

    self.database.query.assert_has_calls([
        call('INSERT INTO user_account_registration (email, token) VALUES (%s, %s) RETURNING id, email, token;', (email.raw, token)),
    ])

  def test_find_account_registration_by_token_queries_database_correctly(self):
    self.database.query().rows = []
    self.repository.find_account_registration_by_token('myToken')
    self.database.query.assert_called_with('SELECT id, email, token FROM user_account_registration WHERE token LIKE %s;', ('myToken',))

class TestPasswordHasher(TestCase):

  def setUp(self):
    self.salt_factory = Mock()
    self.password_hasher = PasswordHasher(self.salt_factory)

  def test_create_salt_hashed_password_returns_salt_from_salt_factory(self):
    salt = 'mySalt'
    password = 'myPassword'
    self.salt_factory.create_salt.return_value = salt

    result = self.password_hasher.create_salt_hashed_password(password)

    expected_hashed_password = hexlify(pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)).decode()
    self.assertEqual(result, (salt, expected_hashed_password))

  def test_hash_password(self):
    hasher = PasswordHasher(Mock())
    hash = '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
    self.assertTrue(hasher.hash_password('password', 'salt') == hash)

class TestPasswordRepository(TestCase):

  def setUp(self):
    self.token_factory = Mock()
    self.database = Mock()
    self.password_hasher = Mock()
    self.salt_factory = Mock()
    self.repository = PasswordRepository(
        self.token_factory,
        self.database,
        self.password_hasher,
    )

  def test_create_password_reset_token_queries_database_correctly(self):
    account = Simple(id=1)
    self.token_factory.create_token.return_value = 'myToken'
    self.database.query.side_effect = [
        Simple(status='INSERT'),
        Simple(rows=[[1, 'some token, hopefully the just inserted one']])
    ]

    self.repository.create_password_reset_token(account)

    insert_call = call('INSERT INTO password_reset_token (user_account_id, token) VALUES (%s, %s) ON CONFLICT (user_account_id) DO UPDATE SET token = excluded.token;', (1, 'myToken'))
    select_call = call('SELECT user_account_id, token FROM password_reset_token WHERE user_account_id = %s;', (account.id,))
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

    self.database.query.assert_called_with('SELECT user_account_id, token FROM password_reset_token WHERE user_account_id = %s;', (account.id,))

  def test_find_password_reset_account_id_queries_database_correctly(self):
    self.database.query.return_value = Simple(rows=[])
    self.repository.find_password_reset_account_id('myToken')
    self.database.query.assert_called_with('SELECT user_account_id FROM password_reset_token WHERE token LIKE %s;', ('myToken',))

  def test_find_password_reset_account_id_parses_response_correctly(self):
    self.database.query.return_value = Simple(rows=[[4]])
    result = self.repository.find_password_reset_account_id('myToken')
    self.assertEqual(result, 4)

  def test_update_password_queries_database_correctly(self):
    self.password_hasher.create_salt_hashed_password.return_value = ('mySalt', 'myHashedPassword')
    self.repository.update_password(4, 'myNewPassword')
    self.database.query.assert_called_with('UPDATE hashed_password SET salt = %s, salted_hash = %s WHERE user_account_id = %s;', ('mySalt', 'myHashedPassword', 4))

  def test_remove_password_reset_token_queries_database_correctly(self):
    self.repository.remove_password_reset_token('myToken')
    self.database.query.assert_called_with('DELETE FROM password_reset_token WHERE token LIKE %s;', ('myToken',))