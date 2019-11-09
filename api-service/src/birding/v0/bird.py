from typing import Optional, List
from sqlalchemy.orm import Session
from .models import BirdThumbnail, Bird


class BirdRepository:

  def __init__(self, sqlalchemy_session: Session):
    self.session = sqlalchemy_session

  def bird_thumbnail(self, bird: Bird) -> Optional[BirdThumbnail]:
    return self.session.query(BirdThumbnail).filter_by(bird_id=bird.id).first()

  def get_bird_by_id(self, id: int) -> Optional[Bird]:
    return self.session.query(Bird).get(id)

  def get_bird_by_binomial_name(self, binomial_name: str) -> Optional[Bird]:
    return self.session.query(Bird).filter(
      Bird.binomial_name.ilike(binomial_name)).first()

  @property
  def birds(self) -> List[Bird]:
    return self.session.query(Bird).all()
