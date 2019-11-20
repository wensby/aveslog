from unittest import TestCase
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from aveslog.v0.localization import Locale
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.models import Bird, Base
from aveslog.v0.search import BirdSearchMatch
from aveslog.v0.search import BirdSearcher
from aveslog.v0.search import StringMatcher

picapica = Bird(binomial_name='Pica pica')


class TestBirdSearcher(TestCase):

  def setUp(self):
    self.string_matcher = StringMatcher()
    self.locale_repository = Mock()
    self.locale_loader = Mock()
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    self.database_session: Session = sessionmaker(bind=engine)()

  def test_search_returns_list_of_bird_matches(self):
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    self.locale_repository.locales = []
    searcher = BirdSearcher(self.database_session, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('Pica pica')

    self.assertIsInstance(matches[0], BirdSearchMatch)

  def test_search_finds_bird_by_binomial_name(self):
    swedish_locale = Locale(id=1, code='sv')
    swedish_loaded_locale = LoadedLocale(swedish_locale, None, None, None)
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    self.locale_repository.locales = [swedish_locale]
    self.locale_repository.find_locale.return_value = swedish_locale
    self.locale_loader.load_locale.return_value = swedish_loaded_locale
    searcher = BirdSearcher(self.database_session, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('Pica pica')

    self.assertEqual(len(matches), 1)

  def test_search_finds_bird_by_swedish_name(self):
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    swedish_locale = Locale(id=1, code='sv')
    swedish_loaded_locale = LoadedLocale(
      swedish_locale, None, {'Pica pica': 'Skata'}, None)
    self.locale_repository.locales = [swedish_locale]
    self.locale_repository.find_locale.return_value = swedish_locale
    self.locale_loader.load_locale.return_value = swedish_loaded_locale
    searcher = BirdSearcher(self.database_session, self.locale_repository,
                            self.string_matcher, self.locale_loader)

    matches = searcher.search('Skata')

    self.assertEqual(len(matches), 1)

  def test_search_finds_none_with_only_empty_string_name_query(self):
    self.database_session.add(Bird(binomial_name='Pica pica'))
    self.database_session.commit()
    searcher = BirdSearcher(self.database_session, self.locale_repository,
                            self.string_matcher, self.locale_loader)

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
