from hashlib import pbkdf2_hmac
from unittest import TestCase
from unittest.mock import Mock
from binascii import hexlify

from aveslog.v0.models import Account, PasswordResetToken
from aveslog.v0.account import PasswordHasher, is_valid_username, \
  is_valid_password


class TestUsername(TestCase):

  def test_invalid_usernames(self):
    self.assertFalse(is_valid_username(''))
    self.assertFalse(is_valid_username('1234'))
    self.assertFalse(is_valid_username('abcde@'))
    self.assertFalse(is_valid_username(''.join(['a'] * 33)))


class TestPassword(TestCase):

  def test_invalid_passwords(self):
    self.assertFalse(is_valid_password(''))
    self.assertFalse(is_valid_password('1234567'))
    self.assertFalse(is_valid_password(''.join(['a'] * 129)))


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


class TestPasswordHasher(TestCase):

  def setUp(self):
    self.salt_factory = Mock()
    self.password_hasher = PasswordHasher(self.salt_factory)

  def test_create_salt_hashed_password_returns_salt_from_salt_factory(self):
    salt = 'mySalt'
    password = 'myPassword'
    self.salt_factory.create_salt.return_value = salt

    result = self.password_hasher.create_salt_hashed_password(password)

    expected_hashed_password = hexlify(
      pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)).decode()
    self.assertEqual(result, (salt, expected_hashed_password))

  def test_hash_password(self):
    hasher = PasswordHasher(Mock())
    hash = '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
    self.assertTrue(hasher.hash_password('password', 'salt') == hash)


class TestPasswordResetToken(TestCase):

  def test_repr(self):
    token = PasswordResetToken(account_id=4, token='token')
    self.assertEqual(repr(token),
      "<PasswordResetToken(account_id='4', token='token')>")

  def test_eq_false_when_other_type(self):
    token = PasswordResetToken(account_id=4, token='token')
    self.assertNotEqual(token, 'PasswordResetToken(4, token)')
