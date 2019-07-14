from datetime import date, time
from http import HTTPStatus

from flask import url_for
from requests_html import HTML

from test_util import AppTestCase


class TestSightingsHomePage(AppTestCase):

  def test_page_contains_expected_content_when_no_sightings(self):
    self.db_insert_account(4, 'myUsername', 'my@email.com', None, None)
    self.set_logged_in(4)

    response = self.client.get('/sighting/')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn(url_for('authentication.logout'), html.links)
    self.assertFalse(html.find('.card'))


class TestCreateSightingForm(AppTestCase):

  def test_get_create_ok(self):
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_person(8)
    self.db_insert_account(15, 'myUsername', 'my@email.com', 8, None)
    self.set_logged_in(15)

    response = self.client.get('/sighting/create/4')

    self.assertEqual(response.status_code, HTTPStatus.OK)

  def test_post_create_redirects_to_login_when_logged_out(self):
    response = self.__post_create(4, '2008-01-05')
    self.assertRedirect(response, 'authentication.get_login')

  def test_post_create_redirects_to_sightings_index_when_logged_in(self):
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_person(8)
    self.db_insert_account(15, 'myUsername', 'my@email.com', 8, None)
    self.set_logged_in(15)

    response = self.__post_create(4, '2016-02-03')

    self.assertRedirect(response, 'sighting.get_sightings')

  def __post_create(self, bird_id, date_input):
    data = {'birdId': bird_id, 'dateInput': date_input}
    return self.client.post(f'/sighting/create/{bird_id}', data=data)


class TestSightingPage(AppTestCase):

  def test_get_sighting_redirects_to_login_when_logged_out(self):
    self.db_insert_person(4)
    self.db_insert_bird(8, 'Pica pica')
    self.db_insert_sighting(15, 4, 8, date(2019, 7, 9), time(19, 10))

    response = self.client.get('/sighting/15')

    self.assertRedirect(response, 'authentication.get_login')

  def test_get_sighting_redirects_home_when_wrong_logged_in_account(self):
    self.db_insert_person(4)
    self.db_insert_person(8)
    self.db_insert_account(15, 'hulot', 'hulot@tati.com', 4, None)
    self.db_insert_bird(16, 'Pica pica')
    self.db_insert_sighting(23, 8, 16, date(2019, 7, 9), time(19, 10))
    self.set_logged_in(15)

    response = self.client.get('/sighting/23')

    self.assertRedirect(response, 'home.index')

  def test_get_sighting_renders_correctly(self):
    self.db_insert_person(4)
    self.db_insert_account(8, 'hulot', 'hulot@tati.com', 4, None)
    self.db_insert_bird(15, 'Pica pica')
    self.db_insert_sighting(16, 4, 15, date(2019, 7, 9), time(19, 10))
    self.set_logged_in(8)

    response = self.client.get('/sighting/16')

    self.assertOkHtmlResponseWith(
      response,
      ".//*[contains(., 'Pica pica') "
      "and .//form[@method = 'post' and .//button[@type = 'submit' "
      "and @value = 'Delete']]]")

  def test_post_delete_sighting_redirects_to_login_when_logged_out(self):
    self.db_insert_person(4)
    self.db_insert_bird(8, 'Pica pica')
    self.db_insert_sighting(15, 4, 8, date(2019, 7, 9), time(19, 10))

    response = self.client.post('/sighting/15', data={'action': 'Delete'})

    self.assertRedirect(response, 'authentication.get_login')

  def test_post_delete_sighting_redirects_home_when_wrong_account(self):
    # When sighting exist but wrong account logged in
    self.db_insert_person(4)
    self.db_insert_account(8, 'hulot', 'hulot@tati.com', 4, None)
    self.db_insert_bird(15, 'Pica pica')
    self.db_insert_sighting(16, 4, 15, date(2019, 7, 9), time(19, 10))
    self.set_logged_in(8)

    response = self.client.post('/sighting/23', data={'action': 'Delete'})

    self.assertRedirect(response, 'home.index')
    self.assertEqual(len(self.db_get_sighting_rows()), 1)

  def test_post_delete_sighting_when_success(self):
    # When sighting exist and correct account logged in
    self.db_insert_person(4)
    self.db_insert_account(8, 'hulot', 'hulot@tati.com', 4, None)
    self.db_insert_bird(15, 'Pica pica')
    self.db_insert_sighting(16, 4, 15, date(2019, 7, 9), time(19, 10))
    self.set_logged_in(8)

    response = self.client.post('/sighting/16', data={'action': 'Delete'})

    self.assertRedirect(response, 'sighting.get_sightings')
    self.assertEqual(len(self.db_get_sighting_rows()), 0)
