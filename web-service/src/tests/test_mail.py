from unittest import TestCase

from birding.mail import EmailAddress


class TestEmailAddress(TestCase):

  def test_construction_when_invalid_format(self):
    self.assertRaises(Exception, EmailAddress, *('invalidformat',))

  def test_eq_false_when_different_type(self):
    self.assertNotEqual(EmailAddress('my@email.com'), 'my@email.com')