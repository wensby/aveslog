from http import HTTPStatus

from flask import url_for
from requests_html import HTML

from test_util import AppTestCase


class TestSettingsPage(AppTestCase):

  def test_settings_index_renders_correctly(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.set_logged_in(4)

    response = self.client.get('/settings/')

    self.assertOkHtmlResponseWith(
      response, f".//a[@href = '{url_for('settings.get_password_settings')}']")


class TestPasswordSettingsPage(AppTestCase):

  def test_password_settings_page_renders_correctly(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.set_logged_in(4)

    response = self.client.get('/settings/password')

    self.assertOkHtmlResponseWith(
      response,
      ".//form[@method = 'post' "
      "and .//input[@name = 'oldPasswordInput'] "
      "and .//input[@name = 'newPasswordInput'] "
      "and .//input[@name = 'newPasswordVerificationInput'] "
      "and .//button[@type = 'submit']]")

  def test_post_password_settings_redirect_to_login_when_not_logged_in(self):
    response = self.client.post(url_for('settings.post_password_settings'))
    self.assertRedirect(response, 'authentication.get_login')

  def test_post_password_settings_flashes_success_when_accurate_old_pwd(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.db_insert_password(4, 'password')
    self.set_logged_in(4)

    response = self.__post_password_settings('password', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn('success', html.full_text)

  def test_post_password_settings_flashes_failure_when_inaccurate_old_pwd(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.db_insert_password(4, 'myPassword')
    self.set_logged_in(4)

    response = self.__post_password_settings('inaccurate', 'newPassword')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn('failure', html.full_text)

  def __post_password_settings(self, password, new_password):
    response = self.client.post(
      url_for('settings.post_password_settings'), data={
        'oldPasswordInput': password,
        'newPasswordInput': new_password,
      })
    return response
