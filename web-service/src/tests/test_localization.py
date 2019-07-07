import unittest
from unittest.mock import Mock

from birding.localization import Locale, LocaleDeterminer


class TestLocale(unittest.TestCase):

  def test_text_returns_argument_when_not_in_dictionary(self):
    locale = Locale('en', dict(), None)
    text = "I'm not in there"
    result = locale.text(text)
    self.assertTrue(result == text)

  def test_text_returns_translation_when_present_in_dictionary(self):
    locale = Locale('en', {"I'm in there": 'Jag är där inne'}, None)
    result = locale.text("I'm in there")
    self.assertTrue(result == 'Jag är där inne')

  def test_text_replaces_variables_if_perfect_match_with_placeholders(self):
    locale = Locale('en', {"Hello {{}}! It is {{}} today.": "Hej {{}}! Det är {{}} idag.", "Monday": "Måndag"}, None)
    result = locale.text("Hello {{}}! It is {{}} today.", ['Lukas', locale.text("Monday")])
    self.assertTrue(result == "Hej Lukas! Det är Måndag idag.")

english_locale = Mock()
swedish_locale = Mock()

class TestLocaleDeterminer(unittest.TestCase):

  def setUp(self):
    self.request = Mock()

  def test_determine_locale_from_request_when_no_cookie(self):
    header_value = 'en-GB,en-US;q=0.9,en;q=0.8,sv;q=0.7'
    self.request.cookies = dict()
    self.request.headers = {'Accept-Language': header_value}
    locales = { 'en': english_locale, 'sv': swedish_locale }
    determiner = LocaleDeterminer('cookie-key', ['en'])
    locale = determiner.determine_locale_from_request(self.request)
    self.assertEqual(locale, 'en')

  def test_determine_locale_from_request_defaults_to_english(self):
    self.request.cookies = dict()
    self.request.headers = dict()
    locales = { 'en': english_locale }
    determiner = LocaleDeterminer('cookie-key', ['en'])
    locale = determiner.determine_locale_from_request(self.request)
    self.assertEqual(locale, 'en')

  def test_determine_locale_from_request_by_cookie(self):
    self.request.cookies = {'cookie-key': 'sv'}
    self.request.headers = {'Accept-Language': 'en'}
    locales = { 'en': english_locale, 'sv': swedish_locale }
    determiner = LocaleDeterminer('cookie-key', ['en', 'sv'])
    locale = determiner.determine_locale_from_request(self.request)
    self.assertEqual(locale, 'sv')
