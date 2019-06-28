from unittest import TestCase

from birding.bird import Bird


class TestBird(TestCase):

  def test_construction(self):
    Bird(4, 'Pica pica')