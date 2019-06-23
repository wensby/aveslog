import os
from hashlib import pbkdf2_hmac
from base64 import b64encode
from unittest import TestCase
from unittest.mock import Mock, call
from types import SimpleNamespace as Simple
from user_account import Authenticator, Credentials, UserAccount, HashedPassword
from user_account import PasswordHasher
from user_account import PasswordRepository
from user_account import PasswordResetToken
from user_account import TokenFactory
from test_util import mock_return
from binascii import hexlify

class TestAuthenticator(TestCase):

  def setUp(self):
    self.repository = Mock()
    self.hasher = Mock()
    self.credentials = Credentials('username', 'password')
    self.account = UserAccount(1, 'username', 'email@wow.com', 1, 1)
    self.hashed_password = HashedPassword(1, 'salt', 'hashed-password')

  def test_get_authenticated_user_account_when_correct_password(self):
    self.repository.find_user_account = mock_return(self.account)
    self.repository.find_hashed_password = mock_return(self.hashed_password)
    self.hasher.hash_password = Mock(return_value='hashed-password')
    authenticator = Authenticator(self.repository, self.hasher)

    authenticated = authenticator.get_authenticated_user_account(self.credentials)

    self.assertEqual(authenticated, self.account)

  def test_get_authenticated_user_account_none_when_wrong_password(self):
    self.repository.find_user_account = mock_return(self.account)
    self.repository.find_hashed_password = mock_return(self.hashed_password)
    self.hasher.hash_password = Mock(return_value='wrong_hash')
    authenticator = Authenticator(self.repository, self.hasher)

    authenticated = authenticator.get_authenticated_user_account(self.credentials)

    self.assertIsNone(authenticated)

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

if __name__ == '__main__':
  unittest.main()
