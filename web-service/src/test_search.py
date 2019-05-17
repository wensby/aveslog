import unittest
from unittest.mock import Mock
from search import BirdSearcher
from bird import Bird
from localization import Language

picapica = Bird(1, 'Pica pica')

class TestBirdSearcher(unittest.TestCase):

  def setUp(self):
    self.bird_repository = Mock()

  def test_search_finds_bird_by_binomial_name(self):
    swedish = Mock()
    swedish_locale = Mock()
    self.bird_repository.birds = [picapica]
    swedish_locale.bird_dictionary = None
    locales = {swedish: swedish_locale}
    searcher = BirdSearcher(self.bird_repository, locales)
    
    matches = searcher.search('Pica pica')

    self.assertTrue(len(matches[picapica]) == 1)

  def test_search_finds_bird_by_swedish_name(self):
    swedish = Mock()
    swedish_locale = Mock()
    self.bird_repository.birds = [picapica]
    bird_dictionary = {'Pica pica': 'Skata'}
    swedish_locale.bird_dictionary = bird_dictionary
    locales = {swedish: swedish_locale}
    searcher = BirdSearcher(self.bird_repository, locales)

    matches = searcher.search('Skata')

    self.assertTrue(len(matches[picapica]) == 1)

if __name__ == '__main__':
  unittest.main()
