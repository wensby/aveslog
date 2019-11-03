from unittest import TestCase
from unittest.mock import Mock

from birding.bird import Bird, BirdThumbnail, BirdRepository

from birding.database import Database
from birding.database import QueryResult
from test_util import mock_database_transaction


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
    BirdThumbnail(4, 8)

  def test_fromrow(self):
    self.assertEqual(BirdThumbnail.fromrow([4, 8]), BirdThumbnail(4, 8))

  def test_repr(self):
    self.assertEqual(
      repr(BirdThumbnail(4, 8)),
      'BirdThumbnail<bird_id=4, picture_id=8>')

  def test_eq(self):
    self.assertEqual(BirdThumbnail(4, 8), BirdThumbnail(4, 8))

  def test_eq_false_when_different_bird_thumbnail(self):
    self.assertNotEqual(BirdThumbnail(4, 8), BirdThumbnail(4, 9))

  def test_eq_false_when_different_type(self):
    self.assertNotEqual(BirdThumbnail(4, 8), 'BirdThumbnail(4, 8)')
