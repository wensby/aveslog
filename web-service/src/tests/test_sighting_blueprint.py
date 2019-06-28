from http import HTTPStatus

from flask import url_for
from requests_html import HTML

from test_util import AppTestCase


class TestSightingBlueprint(AppTestCase):

  def test_get_sightings_index_contains_logout_link_when_logged_in(self):
    self.db_insert_account(4)
    self.populate_session('account_id', 4)

    response = self.client.get(url_for('sighting.get_sightings_index'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn(url_for('authentication.logout'), html.links)

  def test_get_sightings_index_contains_no_sightings_when_logged_in(self):
    self.db_insert_account(4)
    self.populate_session('account_id', 4)

    response = self.client.get(url_for('sighting.get_sightings_index'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertFalse(html.find('.card'))

  def db_insert_account(self, account_id):
    self.app.db.query(
      'INSERT INTO user_account '
      '(id, username, email, person_id, locale_id) '
      'VALUES '
      '(%s, %s, %s, %s, %s);',
      (account_id, 'myUsername', 'myEmail', None, None))
