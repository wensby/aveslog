import unittest
from unittest.mock import Mock
from search import BirdSearcher, BirdMatch
from bird import Bird
from localization import Language

picapica = Bird(1, 'Pica pica')

class TestBirdSearcher(unittest.TestCase):

  def setUp(self):
    self.bird_repository = Mock()

  def test_search_returns_list_of_bird_matches(self):
    self.bird_repository.birds = [picapica]
    searcher = BirdSearcher(self.bird_repository, dict())

    matches = searcher.search('Pica pica')

    self.assertIsInstance(matches[0], BirdMatch)

  def test_search_finds_bird_by_binomial_name(self):
    swedish = Mock()
    swedish_locale = Mock()
    self.bird_repository.birds = [picapica]
    swedish_locale.bird_dictionary = None
    locales = {swedish: swedish_locale}
    searcher = BirdSearcher(self.bird_repository, locales)
    
    matches = searcher.search('Pica pica')

    self.assertTrue(len(matches) == 1)

  def test_search_finds_bird_by_swedish_name(self):
    swedish = Mock()
    swedish_locale = Mock()
    self.bird_repository.birds = [picapica]
    bird_dictionary = {'Pica pica': 'Skata'}
    swedish_locale.bird_dictionary = bird_dictionary
    locales = {swedish: swedish_locale}
    searcher = BirdSearcher(self.bird_repository, locales)

    matches = searcher.search('Skata')

    self.assertTrue(len(matches) == 1)

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
