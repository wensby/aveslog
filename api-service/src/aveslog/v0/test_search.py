from unittest import TestCase

from aveslog.test_util import get_test_database_session
from aveslog.v0.localization import Locale
from aveslog.v0.models import Bird
from aveslog.v0.models import BirdName
from aveslog.v0.search import BirdSearchMatch
from aveslog.v0.search import BirdSearcher
from aveslog.v0.search import StringMatcher

picapica = Bird(binomial_name='Pica pica')


class TestBirdSearcher(TestCase):

  def setUp(self):
    self.string_matcher = StringMatcher()
    self.database_session = get_test_database_session()

  def test_search_returns_list_of_bird_matches(self):
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    searcher = BirdSearcher(self.database_session, self.string_matcher)

    matches = searcher.search('Pica pica')

    self.assertIsInstance(matches[0], BirdSearchMatch)

  def test_search_finds_bird_by_binomial_name(self):
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    searcher = BirdSearcher(self.database_session, self.string_matcher)

    matches = searcher.search('Pica pica')

    self.assertEqual(len(matches), 1)

  def test_search_finds_bird_by_swedish_name(self):
    locale = Locale(code='sv')
    self.database_session.add(locale)
    self.database_session.flush()
    bird = Bird(binomial_name='Pica pica')
    bird.names.append(BirdName(locale_id=locale.id, name='Skata'))
    self.database_session.add(bird)
    self.database_session.commit()
    searcher = BirdSearcher(self.database_session, self.string_matcher)

    matches = searcher.search('Skata')

    self.assertEqual(len(matches), 1)

  def test_search_finds_none_with_only_empty_string_name_query(self):
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    searcher = BirdSearcher(self.database_session, self.string_matcher)

    matches = searcher.search('')

    self.assertEqual(len(matches), 0)


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
