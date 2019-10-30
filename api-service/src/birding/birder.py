from typing import Optional, TypeVar, Type

BirderType = TypeVar('BirderType', bound='Birder')


class Birder:

  def __init__(self, id, name):
    self.id = id
    self.name = name

  @classmethod
  def from_row(cls: Type[BirderType], row: list) -> BirderType:
    return cls(row[0], row[1])


class BirderRepository:

  def __init__(self, database):
    self.database = database

  def containsname(self, name):
    return self.get_birder_by_name(name) is not None

  def fetchonebirder(self, query, vars=None):
    result = self.database.query(query, vars)
    if len(result.rows) == 1:
      return self.birder_from_row(result.rows[0])

  def birder_from_row(self, row):
    return Birder(row[0], row[1])

  def get_birder_by_name(self, name):
    return self.fetchonebirder(
      'SELECT id, name FROM birder WHERE name LIKE %s;', (name,))

  def add_birder(self, name):
    self.database.query('INSERT INTO birder (name) VALUES (%s);', (name,))
    return self.get_birder_by_name(name)

  def birder_by_id(self, birder_id: int) -> Optional[Birder]:
    with self.database.transaction() as transaction:
      result = transaction.execute(
        'SELECT id, name FROM birder WHERE id = %(birder_id)s;',
        {'birder_id': birder_id},
        Birder.from_row)
      return result.rows[0] if result.rows else None
