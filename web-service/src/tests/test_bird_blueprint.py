from test_util import AppTestCase
from flask import url_for
from http import HTTPStatus
from requests_html import HTML

class TestBirdBlueprint(AppTestCase):

  def test_get_bird_contains_bird_binomial_name(self):
    self.db_insert_bird(4, 'Pica pica')

    response = self.client.get(url_for('bird.get_bird', bird_id='4'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn('Pica pica', html.full_text)

  def test_get_bird_contains_bird_locale_name(self):
    self.db_insert_bird(4, 'Pica pica')
    self.db_insert_locale(8, 'sv')
    self.db_insert_account(15, 'alice', None, 8)
    self.set_logged_in(15)

    response = self.client.get(url_for('bird.get_bird', bird_id='4'))

    self.assertEqual(response.status_code, HTTPStatus.OK)
    html = HTML(html=response.data)
    self.assertIn('Skata', html.full_text)
