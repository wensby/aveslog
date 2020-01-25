from http import HTTPStatus

from aveslog.test_util import AppTestCase


class TestGetLocales(AppTestCase):

  def test_get_active_accounts_ok_when_authenticated(self):
    self.db_insert_locale(1, 'sv')
    self.db_insert_locale(2, 'en')

    response = self.client.get('/locales')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'items': [
        'sv',
        'en'
      ],
    })
