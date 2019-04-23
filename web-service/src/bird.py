import json
import psycopg2

class Bird:

  def __init__(self, id, name):
    self.id = id
    self.name = name

class BirdRepository:

  def __init__(self, database):
    self.database = database

  def fetchonebird(self, query, vars=None):
    result = self.database.fetchone(query, vars)
    if result:
      return Bird(result[0], result[1])
    return None

  def get_bird_by_id(self, id):
    return self.fetchonebird("SELECT id, name FROM bird WHERE id = %s;", (id,))

  def get_bird_by_name(self, name):
    return self.fetchonebird("SELECT id, name FROM bird WHERE name like %s;", (name,))

  def add_bird(self, name):
    self.database.fetchone("INSERT INTO bird (name) VALUES (%s);", (name,))
    return self.get_bird_by_name(name)

  def read_birds(self):
    rows = self.database.query("SELECT * FROM bird;")
    birds = []
    for row in rows:
      bird = Bird(row[0], row[1])
      birds.append(bird)
    return birds
