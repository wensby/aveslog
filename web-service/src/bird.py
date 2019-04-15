import json
import psycopg2

class Bird:

  def __init__(self, id, name):
    self.id = id
    self.name = name

class BirdRepository:

  def __init__(self, filepath):
    self.filepath = filepath

  def fetchone(self, query, vars=None):
    result = self.doquery(query, vars)
    if result:
      return result[0]
    else:
      return None

  def doquery(self, query, vars=None):
    connection = psycopg2.connect(host='birding-database-service', dbname="birding-database", user="postgres", password="docker")
    cursor = connection.cursor()
    cursor.execute(query, vars)
    result = None
    try:
      result = cursor.fetchall()
    except:
      pass
    connection.commit()
    cursor.close()
    connection.close()
    return result 

  def fetchonebird(self, query, vars=None):
    result = self.fetchone(query, vars)
    if result:
      return Bird(result[0], result[1])
    return None

  def get_bird_by_id(self, id):
    return self.fetchonebird("SELECT id, name FROM bird WHERE id = %s;", (id,))

  def get_bird_by_name(self, name):
    return self.fetchonebird("SELECT id, name FROM bird WHERE name like %s;", (name,))

  def add_bird(self, name):
    self.fetchone("INSERT INTO bird (name) VALUES (%s);", (name,))
    return self.get_bird_by_name(name)

  def read_birds(self):
    rows = self.doquery("SELECT * FROM bird;")
    birds = []
    for row in rows:
      bird = Bird(row[0], row[1])
      birds.append(bird)
    return birds
