from unittest import TestCase

from birding.birder import Birder


class TestBirder(TestCase):

  def test_construction(self):
    Birder(name='Donald Duck')
