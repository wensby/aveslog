from birding.database import read_script_file
from birding.time import format_date_time


class SightingItem:

  def __init__(self, sighting_id, bird_id, bird_binomial_name, time,
        thumbnail_picture):
    self.sighting_id = sighting_id
    self.bird_id = bird_id
    self.bird_binomial_name = bird_binomial_name
    self.time = time
    self.thumbnail_picture = thumbnail_picture

  def __eq__(self, other):
    if isinstance(other, SightingItem):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self):
    return (f'{self.__class__.__name__}({self.sighting_id}, '
            f'{self.bird_id}, {self.bird_binomial_name}, '
            f'{self.time}, {self.thumbnail_picture})')


class SightingViewFactory:

  def __init__(self, bird_repository, database):
    self.bird_repository = bird_repository
    self.database = database

  def create_sighting_items(self, account):
    query = read_script_file('select_sighting_item_data.sql')
    result = self.database.query(query, (account.person_id,))
    return list(map(self.__create_item, result.rows))

  def __create_item(self, row):
    time = format_date_time(row[3], row[4])
    return SightingItem(row[0], row[1], row[2], time, row[5])

  def create_sighting_creation_view(self, birdid=None):
    bird = self.bird_repository.get_bird_by_id(birdid)
    if bird:
      return SightingCreationView(bird)


class SightingCreationView:

  def __init__(self, bird):
    self.bird = bird

  def __eq__(self, other):
    if isinstance(other, SightingCreationView):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self):
    return f'{self.__class__.__name__}({self.bird})'
