class Sighting:

  def __init__(self, id, person_id, bird_id, sighting_date, sighting_time):
    self.id = id
    self.person_id = person_id
    self.bird_id = bird_id
    self.sighting_date = sighting_date
    self.sighting_time = sighting_time

  def __eq__(self, other):
    if isinstance(other, Sighting):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self):
    return f'{self.__class__.__name__}({self.id}, {self.person_id}, {self.bird_id}, {self.sighting_date}, {self.sighting_time})'


class SightingRepository:

  def __init__(self, database):
    self.database = database

  def find_sighting(self, sighting_id):
    query = ('SELECT id, person_id, bird_id, sighting_date, sighting_time '
             'FROM sighting '
             'WHERE id = %s;')
    result = self.database.query(query, (sighting_id,))
    return next(map(self.sighting_from_row, result.rows), None)

  def delete_sighting(self, sighting_id):
    query = ('DELETE '
             'FROM sighting '
             'WHERE id = %s;')
    result = self.database.query(query, (sighting_id,))
    return 'DELETE' in result.status

  def sighting_from_row(self, row):
    return Sighting(row[0], row[1], row[2], row[3], row[4])

  def add_sighting(self, sighting_post):
    query = (
      'INSERT INTO '
      '  sighting (person_id, bird_id, sighting_date, sighting_time) '
      'VALUES '
      '  (%s, %s, %s, %s);'
    )
    args = (
      sighting_post.person_id,
      sighting_post.bird_id,
      sighting_post.date,
      sighting_post.time,
    )
    result = self.database.query(query, args)
    return 'INSERT 0 1' in result.status


class SightingPost:

  def __init__(self, person_id, bird_id, date, time=None):
    self.person_id = person_id
    self.bird_id = bird_id
    self.date = date
    self.time = time
