import unittest
from unittest.mock import Mock
from user_account import Authenticator, Credentials, UserAccount, HashedPassword
from user_account import PasswordHasher

class TestAuthenticator(unittest.TestCase):

  def setUp(self):
    self.repository = Mock()
    self.hasher = Mock()

  def test_get_authenticated_user_account_when_correct_password(self):
    credentials = Credentials('username', 'password')
    account = UserAccount(1, 'username', 'email@wow.com', 1, 1)
    hash = 'hash'
    hashed_password = HashedPassword(1, 'salt', hash)
    self.repository.find_user_account = Mock(return_value=account)
    self.repository.find_hashed_password = Mock(return_value=hashed_password)
    self.hasher.hash_password = Mock(return_value=hash)
    authenticator = Authenticator(self.repository, self.hasher)
    authenticated = authenticator.get_authenticated_user_account(credentials)
    self.assertTrue(authenticated == account)

  def test_get_authenticated_user_account_none_when_wrong_password(self):
    credentials = Credentials('username', 'password')
    account = UserAccount(1, 'username', 'email@wow.com', 1, 1)
    hashed_password = HashedPassword(1, 'salt', 'correct_hash')
    self.repository.find_user_account = Mock(return_value=account)
    self.repository.find_hashed_password = Mock(return_value=hashed_password)
    self.hasher.hash_password = Mock(return_value='wrong_hash')
    authenticator = Authenticator(self.repository, self.hasher)
    authenticated = authenticator.get_authenticated_user_account(credentials)
    self.assertTrue(authenticated == None)

class TestPasswordHasher(unittest.TestCase):

  def test_hash_password(self):
    hasher = PasswordHasher()
    hash = '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
    self.assertTrue(hasher.hash_password('password', 'salt') == hash)

if __name__ == '__main__':
  unittest.main()
