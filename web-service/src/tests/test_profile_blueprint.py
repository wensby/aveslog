from datetime import date, time

from flask import url_for

from test_util import AppTestCase


class TestProfilePage(AppTestCase):

  def test_own_profile_contains_expected_content(self):
    self.db_insert_account(4, 'hulot', 'hulot@mail.com', None, None)
    self.set_logged_in(4)

    response = self.client.get('/profile/hulot')

    html = self.assertOkHtmlResponse(response)
    self.assertIn('hulot', html.text)

  def test_profile_contains_expected_content_when_logged_out(self):
    self.db_insert_person(1)
    self.db_insert_bird(1, 'Pica pica')
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', 1, None)
    self.db_insert_sighting(1, 1, 1, date(2019, 7, 19), time(20, 40))

    response = self.client.get('/profile/hulot')

    html = self.assertOkHtmlResponse(response)
    self.assertIn('hulot', html.text)
    self.assertEqual(html.find('#lifeListCount', first=True).text, '1')

  def test_profile_redirects_when_account_missing(self):
    response = self.client.get('/profile/missing')
    self.assertRedirect(response, 'home.index')
