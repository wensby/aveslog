from flask import url_for
from test_util import AppTestCase


class TestHomePage(AppTestCase):

  def test_page_contains_expected_content_when_logged_out(self):
    response = self.client.get(url_for('home.index'))
    html = self.assertOkHtmlResponse(response)
    self.assertIn(url_for('authentication.get_login'), html.links)
    self.assertIn(url_for('settings.get_settings_index'), html.links)
    bird_search_form = html.find('form[action="/bird/search"]', first=True)
    self.assertTrue(bird_search_form)
    self.assertEqual(len(bird_search_form.find('input[name="query"]')), 1)
    self.assertEqual(len(bird_search_form.find('button[type="submit"]')), 1)

  def test_page_contains_expected_content_when_logged_in(self):
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', None, None)
    self.set_logged_in(1)

    response = self.client.get(url_for('home.index'))

    html = self.assertOkHtmlResponse(response)
    self.assertEqual(html.find('#headerProfileLink', first=True).attrs['href'],
      url_for('profile.get_profile', username='hulot'))
