from http import HTTPStatus

from flask import url_for
from requests_html import HTML

from test_util import AppTestCase


class TestAuthenticationBlueprint(AppTestCase):

  def test_get_register_request_contains_bird_search(self):
    response = self.client.get(url_for('authentication.get_register_request'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    form = html.find('form#birdSearchForm', first=True)
    self.assertTrue(form)
    self.assertIn(('method', 'get'), form.attrs.items())
    self.assertIn(('action', url_for('search.bird_search')), form.attrs.items())
    self.assertEqual(len(form.find("input[name='query']")), 1)
    self.assertEqual(len(form.find("button[type='submit']")), 1)

  def test_get_register_request_contains_email_submit_form(self):
    response = self.client.get(url_for('authentication.get_register_request'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    form = html.find("form[method='post']", first=True)
    self.assertNotIn('action', form.attrs)
    self.assertEqual(len(form.find('input#emailInput')), 1)
    self.assertEqual(len(form.find("button[type='submit']")), 1)

  def test_get_register_request_contains_link_back_to_login(self):
    response = self.client.get(url_for('authentication.get_register_request'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn(url_for('authentication.get_login'), html.links)

  def test_get_register_request_redirect_when_logged_in(self):
    self.db_insert_account(4)
    self.populate_session('account_id', 4)

    response = self.client.get(url_for('authentication.get_register_request'))

    self.assertRedirect(response, 'home.index')

  def test_post_register_request_flashes_success(self):
    url = url_for('authentication.post_register_request')
    self.client.post(url, data={'email': 'my@email.com'})
    self.assertTrue(self.get_flashed_messages('success'))

  def test_post_register_request_redirects_to_get_register_request(self):
    url = url_for('authentication.post_register_request')
    response = self.client.post(url, data={'email': 'my@email.com'})
    self.assertRedirect(response, 'authentication.get_register_request')
