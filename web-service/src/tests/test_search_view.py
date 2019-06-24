from types import SimpleNamespace as Simple
from unittest import TestCase
from unittest.mock import Mock
from tests.test_util import mock_return
from birding.search_view import BirdSearchViewFactory
from birding.search_view import BirdSearchResultItem

class TestBirdSearchViewFactory(TestCase):

  def setUp(self):
    self.picture_repository = Mock()
    self.bird_repository = Mock()
    self.factory = BirdSearchViewFactory(self.picture_repository, self.bird_repository)

  def test_create_search_result_items_returns_items_based_on_query_match(self):
    bird_a = Simple(id=1)
    bird_b = Simple(id=2)
    good_bird_match = Simple(bird=bird_a, query_match=1)
    worse_bird_match = Simple(bird=bird_b, query_match=0.5)
    bird_matches = [worse_bird_match, good_bird_match]
    self.bird_repository.bird_thumbnails = mock_return([])

    items = self.factory.create_search_result_items(bird_matches)

    self.assertEqual(items[0].bird, bird_a)
    self.assertEqual(items[1].bird, bird_b)

  def test_create_search_result_items_finds_thumbnail_picture(self):
    bird = Simple(id=1)
    picture = Simple(id=2)
    bird_thumbnail = Simple(bird_id=1, picture_id=2)
    bird_match = Simple(bird=bird, query_match=1)
    self.picture_repository.pictures = mock_return([picture])
    self.bird_repository.bird_thumbnails = mock_return([bird_thumbnail])

    items = self.factory.create_search_result_items([bird_match])

    self.assertListEqual(items, [BirdSearchResultItem(bird, picture)])

  def test_create_search_result_items_handles_missing_thumbnail(self):
    bird = Simple(id=1)
    self.picture_repository.pictures = mock_return([])
    self.bird_repository.bird_thumbnails = mock_return([])
    bird_match = Simple(bird=bird, query_match=1)

    items = self.factory.create_search_result_items([bird_match])

    self.assertListEqual(items, [BirdSearchResultItem(bird, None)])
