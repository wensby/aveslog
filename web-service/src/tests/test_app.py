import birding
from flask import url_for
from unittest import TestCase
from test_util import TestClient
from requests_html import HTML


class TestAppCreation(TestCase):

  def test_creation(self):
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    app = birding.create_app(test_config=test_config)

class TestApp(TestCase):

  def setUp(self) -> None:
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    self.app = birding.create_app(test_config=test_config)
    self.app.test_client_class = TestClient

  def test_get_index_ok(self):
    with self.app.test_client() as client:
      response = client.get('/')
      self.assertEqual(response.status_code, 200)

  def test_get_index_contains_login_link(self):
    with self.app.test_client() as client:
      response = client.get('/')
      self.assertLinkPresent(url_for('authentication.get_login'), response)

  def test_get_index_contains_search_form(self):
    with self.app.test_client() as client:
      response = HTML(html=client.get('/').data)
      bird_search_form = response.find('form[action="/bird/search"]')
      self.assertTrue(bird_search_form)
      self.assertTrue(bird_search_form[0].find('input[name="query"]'))
      self.assertTrue(bird_search_form[0].find('button[type="submit"]'))

  def assertLinkPresent(self, url, response):
    self.assertIn(url, HTML(html=response.data).links)