class SightingItem:

  def __init__(self, sighting_id, bird, time, thumbnail_picture):
    self.sighting_id = sighting_id
    self.bird = bird
    self.time = time
    self.thumbnail_picture = thumbnail_picture

  def __eq__(self, other):
    if isinstance(other, SightingItem):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self):
    return ('SightingItem('
        f'sighting_id={self.sighting_id},v'
        f'bird={self.bird}, '
        f'time={self.time}, '
        f'thumbnail_picture={self.thumbnail_picture})')

class SightingViewFactory:

  def __init__(self, bird_repository, picture_repository):
    self.bird_repository = bird_repository
    self.picture_repository = picture_repository

  def create_sighting_items(self, sightings):
    thumbnails = self.bird_repository.bird_thumbnails()
    pictures = self.picture_repository.pictures()
    items = []
    for sighting in sightings:
      bird = self.bird_repository.get_bird_by_id(sighting.bird_id)
      if bird:
        sighting_time = sighting.sighting_date.isoformat()
        if sighting.sighting_time:
          sighting_time = sighting_time + ' ' + sighting.sighting_time.isoformat()
        thumbnail_image = self.find_thumbnail_image(bird, thumbnails, pictures)
        items.append(SightingItem(sighting.id, bird, sighting_time, thumbnail_image))
    items.sort(reverse=True, key=lambda r: r.time)
    return items

  def create_sighting_view(self, sighting):
    bird = self.bird_repository.get_bird_by_id(sighting.bird_id)
    if bird:
      return SightingView(sighting, bird)

  def find_thumbnail_image(self, bird, thumbnails, pictures):
    thumbnail = [x for x in thumbnails if x.bird_id == bird.id]
    if len(thumbnail) < 1:
      return
    thumbnail = thumbnail[0]
    return [x for x in pictures if x.id == thumbnail.picture_id][0]

class SightingView:

  def __init__(self, sighting, bird):
    self.sighting = sighting
    self.bird = bird
