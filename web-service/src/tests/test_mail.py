from unittest import TestCase

from birding.mail import EmailAddress


class TestEmailAddress(TestCase):

  def test_construction_when_invalid_format(self):
    self.assertRaises(Exception, EmailAddress, *('invalidformat',))