from http import HTTPStatus
from flask import url_for
from test_util import AppTestCase
from requests_html import HTML


class TestHomeBlueprint(AppTestCase):

  def test_get_home_contains_login_link_when_logged_out(self):
    response = self.client.get(url_for('home.index'))
    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn(url_for('authentication.get_login'), html.links)

  def test_get_index_contains_search_form(self):
    response = self.client.get(url_for('home.index'))
    html = HTML(html=response.data)
    bird_search_form = html.find('form[action="/bird/search"]', first=True)
    self.assertTrue(bird_search_form)
    self.assertEqual(len(bird_search_form.find('input[name="query"]')), 1)
    self.assertEqual(len(bird_search_form.find('button[type="submit"]')), 1)
