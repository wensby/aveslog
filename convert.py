import json
import os
import io

person_id = 1
people = []
bird_id = 1
birds = []
sighting_id = 1
sightings = []

def get_bird(name):
  global bird_id
  global birds
  birdnames = []
  for bird in birds:
    if bird['name'] == name:
      return bird
  new_bird = {'id': bird_id, 'name': name}
  birds.append(new_bird)
  bird_id = bird_id + 1
  return new_bird

def add_sighting(person_id, bird_id):
  global sighting_id
  global sightings
  sightings.append({'id': sighting_id, 'person_id': person_id, 'bird_id': bird_id})
  sighting_id = sighting_id + 1

for filename in os.listdir('data'):
  if filename.endswith('.txt'):
    person = {'id': person_id, 'name': filename[:-4]}
    people.append(person)
    person_id = person_id + 1
    with io.open('data/' + filename, 'r', encoding='utf-8') as personfile:
      content = personfile.read()
      for line in content.rstrip('\n').split('\n'):
        birdline = line.rstrip()
        bird = get_bird(birdline)
        add_sighting(person['id'], bird['id'])

def createdir(path):
  if not os.path.exists(path):
    os.mkdir(path)

createdir('data/bird')
createdir('data/person')
createdir('data/sighting')

with io.open('data/bird/bird.txt', 'w+', encoding='utf-8') as birdfile:
  for bird in birds:
    birdfile.write(json.dumps(bird) + '\n')

with io.open('data/person/person.txt', 'w+', encoding='utf-8') as personfile:
  for person in people:
    personfile.write(json.dumps(person) + '\n')

with io.open('data/sighting/sighting.txt', 'w+', encoding='utf-8') as sightingfile:
  for sighting in sightings:
    sightingfile.write(json.dumps(sighting) + '\n')
