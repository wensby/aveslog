import json
import psycopg2

class Bird:

  def __init__(self, id, binomial_name):
    self.id = id
    self.binomial_name = binomial_name

  def __eq__(self, other):
    if isinstance(other, Bird):
      return self.__dict__ == other.__dict__
    return False

  def __hash__(self):
    return hash((self.id, self.binomial_name))

class BirdThumbnail:

  def __init__(self, bird_id, picture_id):
    self.bird_id = bird_id
    self.picture_id = picture_id

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1])

  def __repr__(self):
    return \
      f'BirdThumbnail<bird_id={self.bird_id}, picture_id={self.picture_id}>'

  def __eq__(self, other):
    if isinstance(other, BirdThumbnail):
      return self.__dict__ == other.__dict__
    return False

class BirdRepository:

  def __init__(self, database):
    self.database = database

  def fetchonebird(self, query, vars=None):
    result = self.database.query(query, vars)
    if len(result.rows) == 1:
      return self.bird_from_row(result.rows[0])

  def bird_thumbnails(self):
    result = self.database.query('SELECT bird_id, picture_id FROM bird_thumbnail;')
    return list(map(BirdThumbnail.fromrow, result.rows))

  def bird_thumbnail(self, bird):
    query = (
      'SELECT bird_id, picture_id '
      'FROM bird_thumbnail '
      'WHERE bird_id = %s;'
    )
    result = self.database.query(query, (bird.id,))
    return next(map(BirdThumbnail.fromrow, result.rows), None)

  def bird_from_row(self, row):
    return Bird(row[0], row[1])

  def get_bird_by_id(self, id):
    return self.fetchonebird("SELECT id, binomial_name FROM bird WHERE id = %s;", (id,))

  def get_bird_by_binomial_name(self, binomial_name):
    return self.fetchonebird("SELECT id, binomial_name FROM bird WHERE binomial_name ILIKE %s;", (binomial_name,))

  @property
  def birds(self):
    result = self.database.query("SELECT * FROM bird;")
    birds = []
    for row in result.rows:
      bird = Bird(row[0], row[1])
      birds.append(bird)
    return birds
