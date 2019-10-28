from typing import Optional, TypeVar, Type

PersonType = TypeVar('PersonType', bound='Person')


class Person:

  def __init__(self, id, name):
    self.id = id
    self.name = name

  @classmethod
  def from_row(cls: Type[PersonType], row: list) -> PersonType:
    return cls(row[0], row[1])


class PersonRepository:

  def __init__(self, database):
    self.database = database

  def containsname(self, name):
    return self.get_person_by_name(name) is not None

  def fetchoneperson(self, query, vars=None):
    result = self.database.query(query, vars)
    if len(result.rows) == 1:
      return self.person_from_row(result.rows[0])

  def person_from_row(self, row):
    return Person(row[0], row[1])

  def get_person_by_name(self, name):
    return self.fetchoneperson(
      'SELECT id, name FROM person WHERE name LIKE %s;', (name,))

  def add_person(self, name):
    self.database.query('INSERT INTO person (name) VALUES (%s);', (name,))
    return self.get_person_by_name(name)

  def person_by_id(self, person_id: int) -> Optional[Person]:
    with self.database.transaction() as transaction:
      result = transaction.execute(
        'SELECT id, name FROM person WHERE id = %(person_id)s;',
        {'person_id': person_id},
        Person.from_row)
      return result.rows[0] if result.rows else None
