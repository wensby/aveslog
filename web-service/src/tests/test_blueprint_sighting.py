import birding
from flask import url_for
from unittest import TestCase

from test_util import TestClient
from requests_html import HTML


class TestSightingBlueprint(TestCase):

  def setUp(self) -> None:
    test_config = {'TESTING': True, 'SECRET_KEY': 'wowsosecret'}
    self.app = birding.create_app(test_config=test_config)
    self.app.test_client_class = TestClient

  def test_get_sightings_index_contains_logout_link_when_logged_in(self):
    self.insert_db_user_account(1)
    with self.app.test_client() as client:
      self.populate_session(client, 'account_id', 1)
      response = client.get('/sighting/')
      self.assertIn(url_for('authentication.logout'), HTML(html=response.data).links)

  def test_get_sightings_index_contains_no_sightings_when_logged_in(self):
    client = self.app.test_client()
    response = HTML(html=client.get('/sighting').data)
    self.assertFalse(response.find('.card'))

  def populate_session(self, client, key, value):
    with client.session_transaction() as session:
      session[key] = value

  def insert_db_user_account(self, id):
    self.app.db.query(
      'INSERT INTO user_account (id, username, email, person_id, locale_id) VALUES (%s, %s, %s, %s, %s);',
      (id, 'myUsername', 'myEmail', None, None))

  def tearDown(self) -> None:
    self.app.db.query('DELETE FROM user_account;')