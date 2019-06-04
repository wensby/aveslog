class SightingItem:

  def __init__(self, bird, time, thumbnail_picture):
    self.bird = bird
    self.time = time
    self.thumbnail_picture = thumbnail_picture

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
        items.append(SightingItem(bird, sighting_time, thumbnail_image))
    items.sort(reverse=True, key=lambda r: r.time)
    return items

  def find_thumbnail_image(self, bird, thumbnails, pictures):
    thumbnail = [x for x in thumbnails if x.bird_id == bird.id]
    if len(thumbnail) < 1:
      return
    thumbnail = thumbnail[0]
    return [x for x in pictures if x.id == thumbnail.picture_id][0]
