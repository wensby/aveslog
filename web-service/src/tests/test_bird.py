from unittest import TestCase

from birding.bird import Bird, BirdThumbnail


class TestBird(TestCase):

  def test_construction(self):
    Bird(4, 'Pica pica')


class TestBirdThumbnail(TestCase):

  def test_construction(self):
    BirdThumbnail(4, 8)
