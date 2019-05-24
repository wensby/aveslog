from unittest import TestCase
from unittest.mock import Mock
from user_account import Authenticator, Credentials, UserAccount, HashedPassword
from user_account import PasswordHasher
from test_util import mock_return

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

  def test_hash_password(self):
    hasher = PasswordHasher()
    hash = '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
    self.assertTrue(hasher.hash_password('password', 'salt') == hash)

if __name__ == '__main__':
  unittest.main()
