from http import HTTPStatus

from flask import url_for
from requests_html import HTML

from test_util import AppTestCase


class TestSightingBlueprint(AppTestCase):

  def test_get_sightings_index_contains_logout_link_when_logged_in(self):
    self.db_insert_account(4, 'myUsername', None, None)
    self.set_logged_in(4)

    response = self.client.get(url_for('sighting.get_sightings_index'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn(url_for('authentication.logout'), html.links)

  def test_get_sightings_index_contains_no_sightings_when_logged_in(self):
    self.db_insert_account(4, 'myUsername', None, None)
    self.set_logged_in(4)

    response = self.client.get(url_for('sighting.get_sightings_index'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertFalse(html.find('.card'))

  def test_post_sighting_redirects_to_login_when_logged_out(self):
    response = self.__post_sighting(4, '2008-01-05')
    self.assertRedirect(response, 'authentication.get_login')

  def test_post_sighting_redirects_to_sightings_index_when_logged_in(self):
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_person(8)
    self.db_insert_account(15, 'myUsername', 8, None)
    self.set_logged_in(15)

    response = self.__post_sighting(4, '2016-02-03')

    self.assertRedirect(response, 'sighting.get_sightings_index')

  def __post_sighting(self, bird_id, dateInput):
    data = { 'birdId': bird_id, 'dateInput': dateInput }
    return self.client.post(url_for('sighting.post_sighting'), data=data)
