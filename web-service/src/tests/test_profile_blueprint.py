from test_util import AppTestCase


class TestProfilePage(AppTestCase):

  def test_own_profile_contains_expected_content(self):
    self.db_insert_account(4, 'hulot', 'hulot@mail.com', None, None)
    self.set_logged_in(4)

    response = self.client.get('/profile/hulot')

    html = self.assertOkHtmlResponse(response)
    self.assertIn('hulot', html.text)

  def test_profile_contains_expected_content_when_logged_out(self):
    self.db_insert_account(4, 'hulot', 'hulot@mail.com', None, None)

    response = self.client.get('/profile/hulot')

    html = self.assertOkHtmlResponse(response)
    self.assertIn('hulot', html.text)
