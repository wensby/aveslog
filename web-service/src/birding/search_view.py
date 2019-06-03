class BirdSearchResultItem:

  def __init__(self, bird, thumbnail_picture):
    self.bird = bird
    self.thumbnail_picture = thumbnail_picture

  def __eq__(self, obj):
    if isinstance(obj, BirdSearchResultItem):
      return obj.bird == self.bird and obj.thumbnail_picture == self.thumbnail_picture
    else:
      return False

  def __repr__(self):
    return "<BirdSearchResultItem bird:%s thumbnail_picture:%s>" % (self.bird, self.thumbnail_picture)

class BirdSearchViewFactory:

  def __init__(self, picture_repository, bird_repository):
    self.bird_thumbnails = bird_repository.bird_thumbnails()
    self.pictures = picture_repository.pictures()

  def create_search_result_items(self, bird_matches):
    return list(map(self.create_search_result_item, bird_matches))

  def create_search_result_item(self, bird_match):
    bird = bird_match.bird
    thumbnail_picture = self.__thumbnail_picture(bird)
    return BirdSearchResultItem(bird, thumbnail_picture)

  def __thumbnail_picture(self, bird):
    bird_thumbnail = self.__bird_thumbnail(bird)
    if bird_thumbnail:
      return self.__picture(bird_thumbnail.picture_id)

  def __bird_thumbnail(self, bird):
    for bird_thumbnail in self.bird_thumbnails:
      if bird_thumbnail.bird_id == bird.id:
        return bird_thumbnail

  def __picture(self, picture_id):
    for picture in self.pictures:
      if picture.id == picture_id:
        return picture
