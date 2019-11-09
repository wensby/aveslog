from types import SimpleNamespace as Simple
from unittest import TestCase
from unittest.mock import Mock

from birding import BirdSearchController, StringMatcher, BirdSearcher
from birding import Locale, LoadedLocale
from birding.v0.bird import Bird
from birding.search import BirdSearchMatch
from tests.test_util import mock_return

picapica = Bird(binomial_name='Pica pica')


class TestBirdSearchController(TestCase):

  def setUp(self):
    self.searcher = Mock()
    self.controller = BirdSearchController(self.searcher)

  def test_search_return_result_sorted_based_on_score(self):
    search_result = [Simple(bird=Simple(id=i), score=i) for i in range(5)]
    self.searcher.search = mock_return(search_result)

    result = self.controller.search('name', None)

    result_bird_ids = list(map(lambda x: x.bird.id, result))
    self.assertListEqual(result_bird_ids, list(range(0, 5))[::-1])

  def test_search_returns_limited_items(self):
    search_result = [Simple(score=1) for i in range(0, 1000)]
    self.searcher.search = mock_return(search_result)

    result = self.controller.search('name', limit=100)

    self.assertEqual(len(result), 100)


class TestBirdSearcher(TestCase):

  def setUp(self):
    self.string_matcher = StringMatcher()
    self.locale_repository = Mock()
    self.locale_loader = Mock()

  def test_search_returns_list_of_bird_matches(self):
    bird_repository = Simple(birds=[picapica])
    self.locale_repository.locales = []
    searcher = BirdSearcher(bird_repository, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('Pica pica')

    self.assertIsInstance(matches[0], BirdSearchMatch)

  def test_search_finds_bird_by_binomial_name(self):
    swedish_locale = Locale(id=1, code='sv')
    swedish_loaded_locale = LoadedLocale(swedish_locale, None, None, None)
    bird_repository = Simple(birds=[picapica])
    self.locale_repository.locales = [swedish_locale]
    self.locale_repository.find_locale.return_value = swedish_locale
    self.locale_loader.load_locale.return_value = swedish_loaded_locale
    searcher = BirdSearcher(bird_repository, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('Pica pica')

    self.assertEqual(len(matches), 1)

  def test_search_finds_bird_by_swedish_name(self):
    bird_repository = Simple(birds=[picapica])
    swedish_locale = Locale(id=1, code='sv')
    swedish_loaded_locale = LoadedLocale(
      swedish_locale, None, {'Pica pica': 'Skata'}, None)
    self.locale_repository.locales = [swedish_locale]
    self.locale_repository.find_locale.return_value = swedish_locale
    self.locale_loader.load_locale.return_value = swedish_loaded_locale
    searcher = BirdSearcher(bird_repository, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('Skata')

    self.assertEqual(len(matches), 1)

  def test_search_finds_all_with_only_empty_string_name_query(self):
    bird_repository = Simple(birds=[picapica])
    searcher = BirdSearcher(bird_repository, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('')

    self.assertEqual(len(matches), 1)


class TestBirdSearchMatch(TestCase):

  def test_score(self):
    score = 1
    match = BirdSearchMatch(picapica, score)
    self.assertIs(match.score, score)

  def test_bird(self):
    bird = picapica
    match = BirdSearchMatch(bird, 1)
    self.assertIs(match.bird, bird)


class TestStringMatcher(TestCase):

  def test_equal_strings_return_1(self):
    self.assertEqual(StringMatcher().match('test', 'test'), 1)

  def test_equal_strings_return_1_when_different_cases(self):
    self.assertEqual(StringMatcher().match('test', 'TEST'), 1)

  def test_string_with_empty_string_return_0(self):
    self.assertEqual(StringMatcher().match('t', ''), 0)

  def test_string_with_one_out_of_two_matching_chars_returns_half(self):
    self.assertEqual(StringMatcher().match('ab', 'ac'), 0.5)
