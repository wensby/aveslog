from unittest import TestCase
from unittest.mock import Mock

from types import SimpleNamespace as Simple

from birding.birder import Birder, BirderRepository


class TestBirder(TestCase):

  def test_construction(self):
    Birder(4, 'Donald Duck')


class TestBirderRepository(TestCase):

  def setUp(self) -> None:
    self.database = Mock()
    self.repository = BirderRepository(self.database)

  def test_containsname_queries_database_correctly(self):
    self.database.query.return_value = Simple(rows=[])
    self.repository.containsname('myName')
    self.database.query.assert_called_with(
      'SELECT id, name FROM birder WHERE name LIKE %s;', ('myName',))
