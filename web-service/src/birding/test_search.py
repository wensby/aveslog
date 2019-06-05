from types import SimpleNamespace as Mock
import unittest
from search import BirdSearcher, BirdMatch
from bird import Bird
from localization import Language

picapica = Bird(1, 'Pica pica')

class TestBirdSearcher(unittest.TestCase):

  def test_search_returns_list_of_bird_matches(self):
    bird_repository = Mock(birds=[picapica])
    searcher = BirdSearcher(bird_repository, dict())

    matches = searcher.search('Pica pica')

    self.assertIsInstance(matches[0], BirdMatch)

  def test_search_finds_bird_by_binomial_name(self):
    swedish_locale = Mock(bird_dictionary=None)
    bird_repository = Mock(birds=[picapica])
    locales = { 'swedish': swedish_locale }
    searcher = BirdSearcher(bird_repository, locales)
    
    matches = searcher.search('Pica pica')

    self.assertEqual(len(matches), 1)

  def test_search_finds_bird_by_swedish_name(self):
    bird_repository = Mock(birds=[picapica])
    swedish_locale = Mock(bird_dictionary={'Pica pica': 'Skata'})
    locales = { 'swedish': swedish_locale }
    searcher = BirdSearcher(bird_repository, locales)

    matches = searcher.search('Skata')

    self.assertEqual(len(matches), 1)

class TestBirdMatch(unittest.TestCase):

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
