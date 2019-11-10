from unittest import TestCase

from birding.v0.models import BirdThumbnail, Bird


class TestBird(TestCase):

  def test_construction(self):
    Bird(binomial_name='Pica pica')

  def test_eq_when_same_bird(self) -> None:
    self.assertEqual(Bird(binomial_name='Pica pica'), Bird(binomial_name='Pica pica'))

  def test_eq_false_when_other_type(self):
    self.assertNotEqual(Bird(binomial_name='Pica pica'), 'Bird(4, Pica pica)')

  def test_repr(self) -> None:
    self.assertEqual(repr(Bird(binomial_name='Pica pica')), "<Bird(binomial_name='Pica pica')>")


class TestBirdThumbnail(TestCase):

  def test_construction(self):
    BirdThumbnail()

  def test_repr(self):
    self.assertEqual(
      repr(BirdThumbnail()),
      "<BirdThumbnail(bird_id='None', picture_id='None')>")

  def test_eq(self):
    self.assertEqual(BirdThumbnail(), BirdThumbnail())

  def test_eq_false_when_different_bird_thumbnail(self):
    self.assertNotEqual(BirdThumbnail(bird_id=1), BirdThumbnail(bird_id=2))

  def test_eq_false_when_different_type(self):
    self.assertNotEqual(BirdThumbnail(), 'BirdThumbnail(4, 8)')
