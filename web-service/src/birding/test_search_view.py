from types import SimpleNamespace as Mock
from unittest import TestCase
from .test_util import mock_return
from .search_view import BirdSearchViewFactory
from .search_view import BirdSearchResultItem

class TestBirdSearchViewFactory(TestCase):

  def test_create_search_result_items_finds_thumbnail_picture(self):
    bird = Mock(id=1)
    picture = Mock(id=2)
    bird_thumbnail = Mock(bird_id=1, picture_id=2)
    picture_repository = Mock(pictures=mock_return([picture]))
    bird_repository = Mock(bird_thumbnails=mock_return([bird_thumbnail]))
    bird_match = Mock(bird=bird)
    factory = BirdSearchViewFactory(picture_repository, bird_repository)

    items = factory.create_search_result_items([bird_match])

    self.assertListEqual(items, [BirdSearchResultItem(bird, picture)])

  def test_create_search_result_items_handles_missing_thumbnail(self):
    bird = Mock(id=1)
    picture_repository = Mock(pictures=mock_return([]))
    bird_repository = Mock(bird_thumbnails=mock_return([]))
    bird_match = Mock(bird=bird)
    factory = BirdSearchViewFactory(picture_repository, bird_repository)

    items = factory.create_search_result_items([bird_match])

    self.assertListEqual(items, [BirdSearchResultItem(bird, None)])
