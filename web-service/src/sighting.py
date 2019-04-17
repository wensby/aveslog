from pathlib import Path
import json

class Sighting:

  def __init__(self, id, person_id, bird_id):
    self.id = id
    self.person_id = person_id
    self.bird_id = bird_id

class SightingRepository:

  def __init__(self, database):
    self.database = database

  def get_sightings_by_person_id(self, id):
    rows = self.database.doquery('SELECT id, person_id, bird_id FROM sighting WHERE person_id = %s;', (id,))
    sightings = []
    for row in rows:
      sightings.append(Sighting(row[0], row[1], row[2]))
    return sightings

  def add_sighting(self, person_id, bird_id):
    self.database.doquery('INSERT INTO sighting (person_id, bird_id) VALUES (%s, %s);', (person_id, bird_id))
