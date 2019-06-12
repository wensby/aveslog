from unittest import TestCase
from unittest.mock import Mock
from .sighting_view import SightingViewFactory
from .sighting_view import SightingItem
from .test_util import mock_return
from types import SimpleNamespace as Simple
from datetime import datetime

class TestSightingViewFactory(TestCase):

  def setUp(self):
    self.bird_repository = Mock()
    self.picture_repository = Mock()
    self.factory = SightingViewFactory(
        self.bird_repository, self.picture_repository)

  def test_create_sighting_items_returns_empty_list_when_no_sightings(self):
    items = self.factory.create_sighting_items([])
    self.assertListEqual(items, [])

  def test_create_sighting_items_returns_correct_sighting_item(self):
    now = datetime.now()
    date = now.date()
    time = now.time()
    sighting = Simple(id=sighting_id, bird_id=8, sighting_date=date, sighting_time=time)
    bird = Simple(id=8)
    picture = Simple(id=15)
    thumbnail = Simple(bird_id=8, picture_id=15)
    self.bird_repository.get_bird_by_id = mock_return(bird)
    self.bird_repository.bird_thumbnails = mock_return([thumbnail])
    self.picture_repository.pictures = mock_return([picture])

    items = self.factory.create_sighting_items([sighting])

    time = f'{date.isoformat()} {time.isoformat()}'
    self.assertListEqual(items, [SightingItem(4, bird, time, picture)])
