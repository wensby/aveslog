from http import HTTPStatus

from aveslog.test_util import AppTestCase


class TestGetBirderConnection(AppTestCase):

  def test_get_birder_connection_when_ok(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.db_insert_birder_connection(1, 1, 2)
    token = self.create_access_token(1)

    uri = '/birder-connections/1'
    response = self.client.get(uri, headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'id': 1,
      'secondaryBirderId': 2,
    })
