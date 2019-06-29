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
    self.db_insert_account(4, 'myUsername', None)
    self.set_logged_in(4)

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

  def test_get_register_form_redirects_when_logged_in(self):
    self.db_insert_account(4, 'myUsername', None)
    self.set_logged_in(4)

    response = self.__get_register_form('myToken')

    self.assertRedirect(response, 'home.index')

  def test_get_register_form_redirects_when_registration_absent(self):
    response = self.__get_register_form('myToken')
    self.assertRedirect(response, 'authentication.get_register_request')

  def test_get_register_form_flashes_when_registration_absent(self):
    self.__get_register_form('myToken')
    self.assertEqual(
      self.get_flashed_messages(),
      'This registration link is no longer valid, please request a new one.'
    )

  def test_get_register_form_contains_form_when_registration_present(self):
    self.db_insert_registration('my@email.com', 'registrationToken123')
    response = self.__get_register_form('registrationToken123')
    self.__assertRegistrationFormPresent(response)

  def test_post_register_form_redirects_to_home_when_logged_in(self):
    self.db_insert_account(4, 'myUsername', None)
    self.set_logged_in(4)

    response = self.__post_register_form('myToken', None, None, None, None)

    self.assertRedirect(response, 'home.index')

  def test_post_register_form_flashes_success_when_account_created(self):
    self.db_insert_registration('my@email.com', 'myToken')
    self.__post_register_form(
      'myToken', 'my@email.com', 'myToken', 'myUsername', 'myPassword')
    self.assertEqual(
      self.get_flashed_messages('success'), 'User account created successfully')

  def test_post_register_form_flashes_danger_when_token_discrepancy(self):
    self.__post_register_form(
      'myToken', 'my@email.com', 'myToken2', 'myUsername', 'myPassword')
    self.assertEqual(
      self.get_flashed_messages('danger'),
      'Account registraion failure: Registration token discrepancy')

  def test_post_register_form_flashes_danger_when_registration_absent(self):
    self.__post_register_form(
      'myToken', 'my@email.com', 'myToken', 'myUsername', 'myPassword')
    self.assertEqual(
      self.get_flashed_messages('danger'), 'Registration form no longer valid')

  def test_post_register_form_flashes_danger_when_username_taken(self):
    self.db_insert_account(4, 'myTakenUsername', None)
    self.db_insert_registration('my@email.com', 'token')

    self.__post_register_form(
      'token', 'my@email.com', 'token', 'myTakenUsername', 'myPassword')

    self.assertEqual(self.get_flashed_messages('danger'),
                     'Username already taken')

  def __get_register_form(self, token):
    return self.client.get(
      url_for('authentication.get_register_form', token=token)
    )

  def __assertRegistrationFormPresent(self, response):
    self.assertEqual(response.status_code, HTTPStatus.OK)
    xpath = (
      ".//form[@id = 'registrationForm' "
      "and .//input[@name = 'email'] "
      "and .//input[@name = 'username'] "
      "and .//input[@name = 'password'] "
      "and .//input[@name = 'confirmPassword'] "
      "and .//input[@id = 'tocCheckbox'] "
      "and .//button[@type = 'submit']]")
    self.assertTrue(HTML(html=response.data).xpath(xpath, first=True))

  def __post_register_form(self, token, email, form_token, username, password):
    url = url_for('authentication.post_register_form', token=token)
    data = {
      'email': email,
      'token': form_token,
      'username': username,
      'password': password}
    return self.client.post(url, data=data)
