from unittest import TestCase
from unittest.mock import Mock

from birding.localization import Locale, LocaleDeterminer, LoadedLocale


class TestLocale(TestCase):

  def test_eq_false_when_other_type(self):
    self.assertNotEqual(Locale(1, 'en'), 'Locale(1, en)')

  def test_repr(self):
    self.assertEqual(repr(Locale(1, 'en')), 'Locale(1, en)')


class TestLoadedLocale(TestCase):
  locale = Locale(1, 'en')

  def test_text_returns_argument_when_not_in_dictionary(self):
    loaded_locale = LoadedLocale(self.locale, dict(), None, None)
    text = "I'm not in there"
    result = loaded_locale.text(text)
    self.assertTrue(result == text)

  def test_text_returns_translation_when_present_in_dictionary(self):
    loaded_locale = LoadedLocale(
      self.locale, {"I'm in there": 'Jag är där inne'}, None, None)
    result = loaded_locale.text("I'm in there")
    self.assertTrue(result == 'Jag är där inne')

  def test_text_replaces_variables_if_perfect_match_with_placeholders(self):
    loaded_locale = LoadedLocale(self.locale, {
      "Hello {{}}! It is {{}} today.": "Hej {{}}! Det är {{}} idag.",
      "Monday": "Måndag"}, None, None)
    result = loaded_locale.text("Hello {{}}! It is {{}} today.",
                                ['Lukas', loaded_locale.text("Monday")])
    self.assertTrue(result == "Hej Lukas! Det är Måndag idag.")

  def test_records_miss_when_one_miss(self):
    misses_repository = {}
    loaded_locale = LoadedLocale(self.locale, {}, {}, misses_repository)

    loaded_locale.text('missing translation')

    self.assertIn(self.locale, misses_repository)
    self.assertIn('missing translation', misses_repository.get(self.locale))

  def test_records_all_misses_when_several_misses(self):
    misses_repository = {}
    loaded_locale = LoadedLocale(self.locale, {}, {}, misses_repository)

    loaded_locale.text('missing translation')
    loaded_locale.text('another one')

    self.assertIn(self.locale, misses_repository)
    locale_misses = misses_repository.get(self.locale)
    self.assertIn('missing translation', locale_misses)
    self.assertIn('another one', locale_misses)


english_locale = Mock()
swedish_locale = Mock()


class TestLocaleDeterminer(TestCase):

  def setUp(self):
    self.request = Mock()

  def test_determine_locale_from_request_when_no_cookie(self):
    header_value = 'en-GB,en-US;q=0.9,en;q=0.8,sv;q=0.7'
    self.request.cookies = dict()
    self.request.headers = {'Accept-Language': header_value}
    locales = {'en': english_locale, 'sv': swedish_locale}
    determiner = LocaleDeterminer('cookie-key', ['en'])
    locale = determiner.determine_locale_from_request(self.request)
    self.assertEqual(locale, 'en')

  def test_determine_locale_from_request_defaults_to_english(self):
    self.request.cookies = dict()
    self.request.headers = dict()
    locales = {'en': english_locale}
    determiner = LocaleDeterminer('cookie-key', ['en'])
    locale = determiner.determine_locale_from_request(self.request)
    self.assertEqual(locale, 'en')

  def test_determine_locale_from_request_by_cookie(self):
    self.request.cookies = {'cookie-key': 'sv'}
    self.request.headers = {'Accept-Language': 'en'}
    locales = {'en': english_locale, 'sv': swedish_locale}
    determiner = LocaleDeterminer('cookie-key', ['en', 'sv'])
    locale = determiner.determine_locale_from_request(self.request)
    self.assertEqual(locale, 'sv')
