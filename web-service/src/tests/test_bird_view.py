from unittest import TestCase
from unittest.mock import Mock
from types import SimpleNamespace as Simple

from birding.bird_view import BirdViewFactory, BirdPageView


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
