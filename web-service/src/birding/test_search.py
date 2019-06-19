from types import SimpleNamespace as Simple
from unittest import TestCase
from unittest.mock import Mock
from search import BirdSearcher, BirdMatch
from search import BirdSearchController
from bird import Bird
from localization import Language
from test_util import mock_return

picapica = Bird(1, 'Pica pica')

class TestBirdSearchController(TestCase):

  def setUp(self):
    self.searcher = Mock()
    self.controller = BirdSearchController(self.searcher)

  def test_search_return_result_sorted_based_on_query_match(self):
    search_result = [Simple(bird=Simple(id=i), query_match=i) for i in range(5)]
    self.searcher.search = mock_return(search_result)

    result = self.controller.search('name')

    result_bird_ids = list(map(lambda x: x.bird.id, result))
    self.assertListEqual(result_bird_ids, list(range(0, 5))[::-1])

  def test_search_return_result_of_max_100_items(self):
    search_result = [Simple(query_match=1) for i in range(0, 1000)]
    self.searcher.search = mock_return(search_result)

    result = self.controller.search('name')

    self.assertEqual(len(result), 100)

class TestBirdSearcher(TestCase):

  def test_search_returns_list_of_bird_matches(self):
    bird_repository = Simple(birds=[picapica])
    searcher = BirdSearcher(bird_repository, dict())

    matches = searcher.search('Pica pica')

    self.assertIsInstance(matches[0], BirdMatch)

  def test_search_finds_bird_by_binomial_name(self):
    swedish_locale = Simple(bird_dictionary=None)
    bird_repository = Simple(birds=[picapica])
    locales = { 'swedish': swedish_locale }
    searcher = BirdSearcher(bird_repository, locales)
    
    matches = searcher.search('Pica pica')

    self.assertEqual(len(matches), 1)

  def test_search_finds_bird_by_swedish_name(self):
    bird_repository = Simple(birds=[picapica])
    swedish_locale = Simple(bird_dictionary={'Pica pica': 'Skata'})
    locales = { 'swedish': swedish_locale }
    searcher = BirdSearcher(bird_repository, locales)

    matches = searcher.search('Skata')

    self.assertEqual(len(matches), 1)

  def test_search_finds_nothing_with_only_empty_string_name_query(self):
    bird_repository = Simple(birds=[picapica])
    searcher = BirdSearcher(bird_repository, {})

    matches = searcher.search('')

    self.assertEqual(matches, [])

class TestBirdMatch(TestCase):

  def test_query_match(self):
    query_match = 1
    match = BirdMatch(picapica, query_match)
    self.assertIs(match.query_match, query_match)

  def test_bird(self):
    bird = picapica
    match = BirdMatch(bird, 1)
    self.assertIs(match.bird, bird)

if __name__ == '__main__':
  unittest.main()
