import unittest
import birding_locale as locale
from unittest.mock import Mock
from birding_locale import Locale, LocaleDeterminer, LocaleRepository

class TestLocale(unittest.TestCase):

  def test_text_returns_argument_when_not_in_dictionary(self):
    locale = Locale('en', dict())
    text = "I'm not in there"
    result = locale.text(text)
    self.assertTrue(result == text)

  def test_text_returns_translation_when_present_in_dictionary(self):
    locale = Locale('en', {"I'm in there": 'Jag är där inne'})
    result = locale.text("I'm in there")
    self.assertTrue(result == 'Jag är där inne')

  def test_text_replaces_variables_if_perfect_match_with_placeholders(self):
    locale = Locale('en', {"Hello {{}}! It is {{}} today.": "Hej {{}}! Det är {{}} idag.", "Monday": "Måndag"})
    result = locale.text("Hello {{}}! It is {{}} today.", ['Lukas', locale.text("Monday")])
    self.assertTrue(result == "Hej Lukas! Det är Måndag idag.")

class TestLocaleDeterminer(unittest.TestCase):

  def setUp(self):
    repository = Mock()
    repository.languages = Mock(return_value=['en', 'se', 'ko'])
    self.request = Mock()
    self.determiner = LocaleDeterminer(repository)

  def test_figure_out_language_from_request_when_no_cookie(self):
    self.request.cookies = dict()
    self.request.headers = {'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,sv;q=0.7'}
    language = self.determiner.figure_out_language_from_request(self.request)
    self.assertTrue(language == 'en')

  def test_figure_out_language_from_request_defaults_to_english(self):
    self.request.cookies = dict()
    self.request.headers = dict()
    language = self.determiner.figure_out_language_from_request(self.request)
    self.assertTrue(language == 'en')

  def test_figure_out_language_from_request_by_cookie(self):
    self.request.cookies = {'user_lang': 'se'}
    self.request.headers = {'Accept-Language': 'en'}
    language = self.determiner.figure_out_language_from_request(self.request)
    self.assertTrue(language == 'se')

if __name__ == '__main__':
  unittest.main()
