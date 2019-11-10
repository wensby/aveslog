from unittest import TestCase

from v0.models import Birder


class TestBirder(TestCase):

  def test_repr(self):
    donald_duck = Birder(name='Donald Duck')
    self.assertEqual(repr(donald_duck), "<Birder(name='Donald Duck')>")
