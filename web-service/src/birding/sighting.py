from pathlib import Path
import json

class Sighting:

  def __init__(self, id, person_id, bird_id, sighting_date, sighting_time):
    self.id = id
    self.person_id = person_id
    self.bird_id = bird_id
    self.sighting_date = sighting_date
    self.sighting_time = sighting_time

class SightingRepository:

  def __init__(self, database):
    self.database = database

  def get_sightings_by_person_id(self, id):
    query = ('SELECT id, person_id, bird_id, sighting_date, sighting_time '
             'FROM sighting '
             'WHERE person_id = %s;')
    result = self.database.query(query, (id,))
    return list(map(self.sighting_from_row, result.rows))

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
    return self.database.query(query, args)

class SightingPost:

  def __init__(self, person_id, bird_id, date, time=None):
    self.person_id = person_id
    self.bird_id = bird_id
    self.date = date
    self.time = time
