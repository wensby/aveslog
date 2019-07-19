from test_util import AppTestCase


class TestLocalization(AppTestCase):

  def test_get_language_redirects_home(self):
    response = self.client.get('/language?l=sv')
    self.assertRedirect(response, 'home.index')

  def test_get_language_when_logged_in(self):
    self.db_insert_locale(1, 'sv')
    self.db_insert_account(1, 'hulot', 'hulot@mail.com', None, None)
    self.set_logged_in(1)

    self.client.get('/language?l=sv')

    self.assertEqual(self.db_get_account(1).locale_id, 1)

  def test_saves_locales_misses_after_request(self):
    self.db_insert_locale(1, 'xx')
    headers = {'Accept-Language': 'xx'}

    self.client.get('/', headers=headers)

    self.assertFileExist('test-logs/locales-misses/xx.txt')