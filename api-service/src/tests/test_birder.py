from unittest import TestCase

from birding.v0.models import Birder


class TestBirder(TestCase):

  def test_construction(self):
    Birder(name='Donald Duck')
