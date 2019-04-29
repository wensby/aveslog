from pathlib import Path
import json

class Sighting:

  def __init__(self, id, person_id, bird_id, sighting_time):
    self.id = id
    self.person_id = person_id
    self.bird_id = bird_id
    self.sighting_time = sighting_time

  def from_row(row):
    return Sighting(row[0], row[1], row[2], row[3])

class SightingRepository:

  def __init__(self, database):
    self.database = database

  def get_sightings_by_person_id(self, id):
    query = ('SELECT id, person_id, bird_id, sighting_time '
             'FROM sighting '
             'WHERE person_id = %s;')
    rows = self.database.query(query, (id,))
    return map(Sighting.from_row, rows)

  def add_sighting(self, person_id, bird_id, sighting_time):
    query = ('INSERT INTO sighting (person_id, bird_id, sighting_time) '
             'VALUES (%s, %s, %s);')
    self.database.query(query, (person_id, bird_id, sighting_time))
