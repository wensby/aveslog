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
    self.bird_repository = bird_repository
    self.picture_repository = picture_repository

  def create_search_result_items(self, bird_matches):
    bird_thumbnails = self.bird_repository.bird_thumbnails()
    pictures = self.picture_repository.pictures()
    builder = BirdSearchResultItemsBuilder(bird_thumbnails, pictures)
    bird_matches = sorted(bird_matches, key=lambda m: m.query_match, reverse=True)
    for bird_match in bird_matches:
      builder.add_bird_match(bird_match)
    return builder.create_items()

class BirdSearchResultItemsBuilder:

  def __init__(self, bird_thumbnails, pictures):
    self.__bird_thumbnails = bird_thumbnails
    self.__pictures = pictures
    self.__bird_matches = []

  def add_bird_match(self, bird_match):
    self.__bird_matches.append(bird_match)

  def create_items(self):
    return list(map(self.__to_item, self.__bird_matches))

  def __to_item(self, bird_match):
    bird = bird_match.bird
    thumbnail_picture = self.__thumbnail_picture(bird)
    return BirdSearchResultItem(bird, thumbnail_picture)

  def __thumbnail_picture(self, bird):
    bird_thumbnail = self.__bird_thumbnail(bird)
    if bird_thumbnail:
      return self.__picture(bird_thumbnail.picture_id)

  def __bird_thumbnail(self, bird):
    for bird_thumbnail in self.__bird_thumbnails:
      if bird_thumbnail.bird_id == bird.id:
        return bird_thumbnail

  def __picture(self, picture_id):
    for picture in self.__pictures:
      if picture.id == picture_id:
        return picture
