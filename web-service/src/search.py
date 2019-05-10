class BirdSearcher:

  def __init__(self, bird_repository):
    self.bird_repository = bird_repository

  def search(self, name=None):
    birds = self.bird_repository.birds
    if name:
      return list(filter(lambda x: name.lower() in x.name.lower(), birds))
