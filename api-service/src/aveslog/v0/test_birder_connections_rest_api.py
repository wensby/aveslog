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

  def test_get_birder_connection_when_missing(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    uri = '/birder-connections/1'
    headers = {'accessToken': self.create_access_token(1).jwt}

    response = self.client.get(uri, headers=headers)

    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestDeleteBirderConnection(AppTestCase):

  def test_delete_birder_connection_when_ok(self):
    self.db_setup_account(1, 1, 'kenny.bostick', 'myPassword', 'kenny@mail.com')
    self.db_insert_birder(2, 'Brad Harris')
    self.db_insert_birder_connection(1, 1, 2)
    token = self.create_access_token(1)

    uri = '/birder-connections/1'
    response = self.client.delete(uri, headers={'accessToken': token.jwt})

    self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
    self.assertIsNone(response.json)
    db_birder_connections = self.db_get_birder_connections()
    self.assertListEqual(db_birder_connections, [])
