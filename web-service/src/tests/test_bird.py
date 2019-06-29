from unittest import TestCase

from birding.bird import Bird, BirdThumbnail


class TestBird(TestCase):

  def test_construction(self):
    Bird(4, 'Pica pica')


class TestBirdThumbnail(TestCase):

  def test_construction(self):
    BirdThumbnail(4, 8)

  def test_fromrow(self):
    self.assertEqual(BirdThumbnail.fromrow([4, 8]), BirdThumbnail(4, 8))

  def test_repr(self):
    self.assertEqual(
      repr(BirdThumbnail(4, 8)),
      'BirdThumbnail<bird_id=4, picture_id=8>')

  def test_eq(self):
    self.assertEqual(BirdThumbnail(4, 8), BirdThumbnail(4, 8))

  def test_eq_false(self):
    self.assertNotEqual(BirdThumbnail(4, 8), BirdThumbnail(4, 9))