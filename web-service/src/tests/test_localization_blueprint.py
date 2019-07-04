from test_util import AppTestCase

class TestLocalizationBlueprint(AppTestCase):

  def test_get_language_redirects_home(self):
    response = self.client.get('/language?l=sv')
    self.assertRedirect(response, 'home.index')