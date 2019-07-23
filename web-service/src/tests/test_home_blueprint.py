from flask import url_for
from test_util import AppTestCase


class TestHomePage(AppTestCase):

  def test_ok_when_logged_out(self):
    response = self.client.get(url_for('home.index'))
    self.assertOkHtmlResponse(response)

  def test_ok_when_logged_in(self):
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', None, None)
    self.set_logged_in(1)

    response = self.client.get(url_for('home.index'))

    html = self.assertOkHtmlResponse(response)
