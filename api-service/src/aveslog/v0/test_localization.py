import os
import shutil
import tempfile
from typing import Set
from unittest import TestCase
from unittest.mock import Mock

from sqlalchemy.orm import Session

from aveslog.v0.localization import LocaleDeterminer
from aveslog.v0.localization import LoadedLocale
from aveslog.v0.localization import Locale
from aveslog.v0.localization import LocaleRepository
from aveslog.v0.localization import LocaleLoader


class TestLocale(TestCase):

  def test_eq_false_when_other_type(self):
    self.assertNotEqual(Locale(id=1, code='en'), 'Locale(1, en)')

  def test_eq_true_when_other_equal_instance(self):
    self.assertEqual(Locale(id=1, code='en'), Locale(id=1, code='en'))

  def test_repr(self):
    self.assertEqual(repr(Locale(id=1, code='en')), "<Locale(code='en')>")


class TestLoadedLocale(TestCase):
  locale = Locale(id=1, code='en')

  def test_text_returns_argument_when_not_in_dictionary(self):
    loaded_locale = LoadedLocale(self.locale, dict())
    text = "I'm not in there"
    result = loaded_locale.text(text)
    self.assertTrue(result == text)

  def test_text_returns_translation_when_present_in_dictionary(self):
    loaded_locale = LoadedLocale(
      self.locale, {"I'm in there": 'Jag är där inne'})
    result = loaded_locale.text("I'm in there")
    self.assertTrue(result == 'Jag är där inne')

  def test_text_replaces_variables_if_perfect_match_with_placeholders(self):
    loaded_locale = LoadedLocale(self.locale, {
      "Hello {{}}! It is {{}} today.": "Hej {{}}! Det är {{}} idag.",
      "Monday": "Måndag"})
    result = loaded_locale.text("Hello {{}}! It is {{}} today.",
                                ['Lukas', loaded_locale.text("Monday")])
    self.assertTrue(result == "Hej Lukas! Det är Måndag idag.")


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


class TestLocaleRepository(TestCase):

  def setUp(self) -> None:
    self.loader = Mock(spec=LocaleLoader)
    self.session = Mock(spec=Session)
    self.temp_dir = tempfile.mkdtemp()

  def test_available_locale_codes_when_multiple(self) -> None:
    codes = {'en', 'sv', 'ko'}
    self.create_temporary_locale_directories(codes)
    repository = LocaleRepository(self.temp_dir, self.loader)

    result = repository.available_locale_codes()

    self.assertSetEqual(result, codes)

  def test_available_locale_codes_when_none(self) -> None:
    repository = LocaleRepository(self.temp_dir, self.loader)
    result = repository.available_locale_codes()
    self.assertSetEqual(result, set())

  def test_available_locale_codes_when_locales_directory_missing(self) -> None:
    repository = LocaleRepository('missing_dir', self.loader)
    result = repository.available_locale_codes()
    self.assertSetEqual(result, set())

  def create_temporary_locale_directories(self, codes: Set[str]) -> None:
    for code in codes:
      os.mkdir(os.path.join(self.temp_dir, code))

  def tearDown(self) -> None:
    shutil.rmtree(self.temp_dir)
