class BirdViewFactory:

  def __init__(self, bird_repository, picture_repository):
    self.bird_repository = bird_repository
    self.picture_repository = picture_repository

  def create_bird_page_view(self, bird_id=None, binomial_name=None):
    if bird_id:
      bird = self.bird_repository.get_bird_by_id(bird_id)
    else:
      bird = self.bird_repository.get_bird_by_binomial_name(binomial_name)
    cover_picture = self.get_cover(bird)
    thumbnail_picture = self.get_thumbnail(bird)
    return BirdPageView(bird, cover_picture, thumbnail_picture)

  def get_thumbnail(self, bird):
    thumbnail = self.bird_repository.bird_thumbnail(bird)
    if thumbnail:
      pictures = self.picture_repository.pictures()
      return [x for x in pictures if x.id == thumbnail.picture_id][0]

  def get_cover(self, bird):
    return self.get_thumbnail(bird)

class BirdPageView:

  def __init__(self, bird, cover_picture, thumbnail_picture):
    self.bird = bird
    self.cover_picture = cover_picture
    self.thumbnail_picture = thumbnail_picture

  def __eq__(self, other):
    if isinstance(other, BirdPageView):
      return self.__dict__ == other.__dict__
    return False
