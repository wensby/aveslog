from unittest import TestCase
from unittest.mock import Mock

from birding.bird import Bird, BirdThumbnail, BirdRepository

from types import SimpleNamespace as Simple


class TestBird(TestCase):

  def test_construction(self):
    Bird(4, 'Pica pica')

  def test_eq_false_when_other_type(self):
    self.assertNotEqual(Bird(4, 'Pica pica'), 'Bird(4, Pica pica)')


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


class TestBirdRepository(TestCase):

  def setUp(self) -> None:
    self.database = Mock()
    self.repository = BirdRepository(self.database)

  def test_fetchonebird_queries_database_correctly(self):
    self.database.query.return_value = Simple(rows=[])
    self.repository.fetchonebird('query', (1,))
    self.database.query.assert_called_with('query', (1,))

  def test_fetchonebird_parses_result_correctly(self):
    self.database.query.return_value = Simple(rows=[[4, 'Pica pica']])
    result = self.repository.fetchonebird('query', (4,))
    self.assertEqual(result, Bird(4, 'Pica pica'))
