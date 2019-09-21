class Person:

  def __init__(self, id, name):
    self.id = id
    self.name = name


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
