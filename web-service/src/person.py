import json

class Person:

  def __init__(self, id, name):
    self.id = id
    self.name = name

class PersonRepository:

  def __init__(self, repository_filepath):
    self.repository_filepath = repository_filepath

  def containsname(self, name):
    return self.get_person_by_name(name) is not None

  def get_person_by_name(self, name):
    people = self.get_people()
    for person in people:
      if person.name == name:
        return person
    return None

  def get_people(self):
    people = []
    with self.repository_filepath.open('r') as repository_file:
      for line in repository_file:
        print(line)
        person_dict = json.loads(line.rstrip())
        people.append(Person(person_dict['id'], person_dict['name']))
    return people

  def get_next_person_id(self):
    people = self.get_people()
    ids = []
    for person in people:
      ids.append(person.id)
    person_id = 0
    while person_id in ids:
      person_id = person_id + 1
    return person_id

  def add_person(self, name):
    person_id = self.get_next_person_id()
    person = Person(person_id, name)
    with self.repository_filepath.open('a') as repository_file:
      repository_file.write(json.dumps(person.__dict__) + '\n')
    return person
