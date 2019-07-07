from test_util import AppTestCase
from flask import url_for


class TestBirdBlueprint(AppTestCase):

  def test_get_bird_by_binomial_name_contains_binomial_name(self):
    self.db_insert_bird(4, 'Pica pica')
    response = self.client.get('/bird/pica_pica')
    self.assertOkHtmlResponseWithText(response, 'Pica pica')

  def test_get_bird_contains_bird_binomial_name(self):
    self.db_insert_bird(4, 'Pica pica')
    response = self.client.get(url_for('bird.get_bird', bird_id='4'))
    self.assertOkHtmlResponseWithText(response, 'Pica pica')

  def test_get_bird_contains_bird_locale_name_when_locale_available_and_set_on_logged_in_account(self):
    self.assertFileExist('birding/locales/sv/sv-bird-names.json')
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_locale(8, 'sv')
    self.db_insert_account(15, 'alice', None, 8)
    self.set_logged_in(15)

    response = self.client.get(url_for('bird.get_bird', bird_id='4'))

    self.assertOkHtmlResponseWithText(response, 'Skata')

  def test_get_bird_without_locale_name_when_not_set_on_logged_in_account(self):
    self.assertFileExist('birding/locales/sv/sv-bird-names.json')
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_locale(8, 'sv')
    self.db_insert_account(15, 'alice', None, None)
    self.set_logged_in(15)

    response = self.client.get(url_for('bird.get_bird', bird_id='4'))

    self.assertOkHtmlResponseWithoutText(response, 'Skata')

  def test_get_bird_contains_locale_bird_name_when_locale_available_enabled_and_in_request_headers(self):
    self.assertFileExist('birding/locales/sv/sv-bird-names.json')
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_locale(8, 'sv')
    headers = {'Accept-Language': 'sv'}

    response = self.client.get(
      url_for('bird.get_bird', bird_id='4'), headers=headers)

    self.assertOkHtmlResponseWithText(response, 'Skata')

  def test_get_bird_not_contains_locale_bird_name_when_locale_available_and_in_request_headers_but_not_in_database(self):
    self.assertFileExist('birding/locales/sv/sv-bird-names.json')
    self.db_insert_bird(4, 'Pica pica')
    headers = {'Accept-Language': 'sv'}

    response = self.client.get(
      url_for('bird.get_bird', bird_id='4'), headers=headers)

    self.assertOkHtmlResponseWithoutText(response, 'Skata')