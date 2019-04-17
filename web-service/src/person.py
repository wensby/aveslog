import json
import psycopg2

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
    result = self.database.fetchone(query, vars)
    if result:
      return Person(result[0], result[1])
    return None

  def get_person_by_name(self, name):
    return self.fetchoneperson('SELECT id, name FROM person WHERE name like %s;', (name,))

  def get_people(self):
    rows = self.database.doquery('SELECT * FROM person;')
    people = []
    for row in rows:
      person = Person(row[0], row[1])
      people.append(bird)
    return people

  def add_person(self, name):
    self.database.fetchone('INSERT INTO person (name) VALUES (%s);', (name,))
    return self.get_person_by_name(name)
