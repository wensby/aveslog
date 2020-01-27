from http import HTTPStatus

from aveslog.test_util import AppTestCase


class TestGetRolesPermissions(AppTestCase):

  def test_get_roles_permissions_when_ok(self):
    self.db_insert_role(1, 'admin')

    response = self.client.get('/roles/admin/permissions')

    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertDictEqual(response.json, {
      'id': 1,
      'name': 'admin',
    })