import json
import psycopg2

class Bird:

  def __init__(self, id, binomial_name):
    self.id = id
    self.binomial_name = binomial_name

class BirdRepository:

  def __init__(self, database):
    self.database = database

  def fetchonebird(self, query, vars=None):
    result = self.database.query(query, vars)
    if result:
      return Bird(result[0][0], result[0][1])

  def get_bird_by_id(self, id):
    return self.fetchonebird("SELECT id, binomial_name FROM bird WHERE id = %s;", (id,))

  def get_bird_by_binomial_name(self, binomial_name):
    return self.fetchonebird("SELECT id, binomial_name FROM bird WHERE binomial_name like %s;", (name,))

  @property
  def birds(self):
    rows = self.database.query("SELECT * FROM bird;")
    birds = []
    for row in rows:
      bird = Bird(row[0], row[1])
      birds.append(bird)
    return birds
