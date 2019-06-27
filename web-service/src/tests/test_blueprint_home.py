from http import HTTPStatus
from flask import url_for
from test_util import AppTestCase
from requests_html import HTML


class TestHomeBlueprint(AppTestCase):

  def test_get_home_contains_login_link_when_logged_out(self):
    with self.app.test_client() as client:
      response = client.get('/')
      self.assertEqual(response.status_code, HTTPStatus.OK)
      html = HTML(html=response.data)
      self.assertIn(url_for('authentication.get_login'), html.links)

  def test_get_index_contains_search_form(self):
    with self.app.test_client() as client:
      response = client.get('/')
      html = HTML(html=response.data)
      bird_search_form = html.find('form[action="/bird/search"]')
      self.assertTrue(bird_search_form)
      self.assertTrue(bird_search_form[0].find('input[name="query"]'))
      self.assertTrue(bird_search_form[0].find('button[type="submit"]'))