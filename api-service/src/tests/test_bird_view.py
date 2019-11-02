from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple

from birding.bird import Bird
from birding.bird_view import BirdViewFactory, BirdPageView
from birding.picture import Picture


class TestBirdViewFactory(TestCase):

  def setUp(self):
    self.picture_repository = Mock()
    self.bird_repository = Mock()
    self.factory = BirdViewFactory(
      self.bird_repository,
      self.picture_repository,
    )

  def test_create_bird_page_view_returns_correct_page_view(self):
    bird = self.bird_repository.get_bird_by_id()
    thumbnail_picture = self.bird_repository.bird_thumbnail()
    picture = Simple(id=thumbnail_picture.picture_id)
    self.picture_repository.pictures.return_value = [picture]

    page_view = self.factory.create_bird_page_view(bird_id=4)

    self.assertEqual(page_view, BirdPageView(bird, picture, picture))
    self.bird_repository.get_bird_by_id.assert_called_with(4)
    self.bird_repository.bird_thumbnail.assert_called_with(bird)
    self.picture_repository.pictures.assert_called()

  def test_eq_false_when_other_type(self):
    bird = Bird(4, 'Pica pica')
    cover_picture = Picture(filepath='filepath1', credit='credit1')
    thumbnail_picture = Picture(filepath='filepath2', credit='credit2')
    page_view = BirdPageView(bird, cover_picture, thumbnail_picture)
    self.assertNotEqual(
      page_view,
      'BirdPageView('
      'Bird(4, Pica pica,) '
      'Picture(8, filepath1, credit1), '
      'Picture(15, filepath2, credit2))')
