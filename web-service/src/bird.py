import json

class Bird:

  def __init__(self, id, name):
    self.id = id
    self.name = name

class BirdRepository:

  def __init__(self, filepath):
    self.filepath = filepath

  def get_bird_by_id(self, id):
    for bird in self.read_birds():
      if bird.id == id:
        return bird
    return None

  def get_bird_by_name(self, name):
    for bird in self.read_birds():
      if bird.name == name:
        return bird
    return None

  def add_bird(self, name):
    birds = self.read_birds()
    bird_id = self.get_unused_bird_id(birds)
    bird = Bird(bird_id, name)
    with self.filepath.open('a') as birdfile:
      birdfile.write(json.dumps(bird.__dict__) + '\n')
    return bird

  def read_birds(self):
    birds = []
    with self.filepath.open('r') as birdfile:
      for line in birdfile:
        bird_dict = json.loads(line.rstrip())
        bird = Bird(bird_dict['id'], bird_dict['name'])
        birds.append(bird)
    return birds

  def get_unused_bird_id(self, birds):
    ids = []
    for bird in birds:
      ids.append(bird.id)
    id = 0
    while id in ids:
      id = id + 1
    return id
