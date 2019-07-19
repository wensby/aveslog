from flask import url_for
from test_util import AppTestCase


class TestHomePage(AppTestCase):

  def test_page_contains_expected_content_when_logged_out(self):
    response = self.client.get(url_for('home.index'))
    html = self.assertOkHtmlResponse(response)
    self.assertIn(url_for('authentication.get_login'), html.links)
    bird_search_form = html.find('form[action="/bird/search"]', first=True)
    self.assertTrue(bird_search_form)
    self.assertEqual(len(bird_search_form.find('input[name="query"]')), 1)
    self.assertEqual(len(bird_search_form.find('button[type="submit"]')), 1)
