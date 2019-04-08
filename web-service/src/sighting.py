from pathlib import Path
import json

class Sighting:

  def __init__(self, id, person_id, bird_id):
    self.id = id
    self.person_id = person_id
    self.bird_id = bird_id

class SightingRepository:

  def __init__(self, sighting_file):
    self.sighting_file = sighting_file

  def get_sightings_by_person_id(self, id):
    sightings = []
    for sighting in self.read_sightings():
      if sighting.person_id == id:
        sightings.append(sighting)
    return sightings

  def read_sightings(self):
    sightings = []
    with self.sighting_file.open('r') as file:
      for line in file:
        strippedline = line.rstrip()
        json_dict = json.loads(strippedline)
        sightings.append(Sighting(json_dict['id'], json_dict['person_id'], json_dict['bird_id']))
    return sightings

  def find_unused_id(self, sightings):
    ids = []
    for sighting in sightings:
      ids.append(sighting.id)
    id = 0
    while id in ids:
      id = id + 1
    return id

  def add_sighting(self, person_id, bird_id):
    sightings = self.read_sightings()
    unused_id = self.find_unused_id(sightings)
    new_sighting = Sighting(unused_id, person_id, bird_id)
    with self.sighting_file.open('a') as file:
      file.write(json.dumps(new_sighting.__dict__) + '\n')
    return new_sighting

  def get_sightings(self, person_id):
    sightings = self.read_sightings()
    return filter(lambda sighting : sighting.person_id == person_id, sightings)
