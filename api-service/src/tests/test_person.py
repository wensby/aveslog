from unittest import TestCase
from unittest.mock import Mock

from types import SimpleNamespace as Simple

from birding.person import Person, PersonRepository


class TestPerson(TestCase):

  def test_construction(self):
    Person(4, 'Donald Duck')


class TestPersonRepository(TestCase):

  def setUp(self) -> None:
    self.database = Mock()
    self.repository = PersonRepository(self.database)

  def test_containsname_queries_database_correctly(self):
    self.database.query.return_value = Simple(rows=[])
    self.repository.containsname('myName')
    self.database.query.assert_called_with(
      'SELECT id, name FROM person WHERE name LIKE %s;', ('myName',))
