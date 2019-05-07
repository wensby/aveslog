import unittest
import birding_locale as locale
from unittest.mock import Mock

class TestLocale(unittest.TestCase):

  def setUp(self):
    pass

  def test_figure_out_language_from_request_when_no_cookie(self):
    request = Mock()
    request.cookies = dict()
    request.headers = {'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,sv;q=0.7'}
    language = locale.figure_out_language_from_request(request)
    self.assertTrue(language == 'en')

  def test_figure_out_language_from_request_defaults_to_english(self):
    request = Mock()
    request.cookies = dict()
    request.headers = dict()
    language = locale.figure_out_language_from_request(request)
    self.assertTrue(language == 'en')

  def test_figure_out_language_from_request_by_cookie(self):
    request = Mock()
    request.cookies = {'user_lang': 'se'}
    request.headers = {'Accept-Language': 'en'}
    language = locale.figure_out_language_from_request(request)
    self.assertTrue(language == 'se')

if __name__ == '__main__':
  unittest.main()
