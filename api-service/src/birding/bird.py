from typing import Any, Optional, List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from .sqlalchemy_database import Base


class Bird(Base):
  __tablename__ = 'bird'
  id = Column(Integer, primary_key=True)
  binomial_name = Column(String, nullable=False)
  thumbnail = relationship('BirdThumbnail', uselist=False)

  def __eq__(self, other: Any):
    if isinstance(other, Bird):
      return self.id == other.id and self.binomial_name == other.binomial_name
    return False

  def __repr__(self):
    return f"<Bird(binomial_name='{self.binomial_name}')>"

  def __hash__(self) -> int:
    return hash((self.id, self.binomial_name))


class BirdThumbnail(Base):
  __tablename__ = 'bird_thumbnail'
  bird_id = Column(Integer, ForeignKey('bird.id'), primary_key=True)
  picture_id = Column(Integer, ForeignKey('picture.id'))
  bird = relationship('Bird', back_populates='thumbnail')
  picture = relationship('Picture')

  def __repr__(self) -> str:
    return \
      f"<BirdThumbnail(bird_id='{self.bird_id}', picture_id='{self.picture_id}')>"

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, BirdThumbnail):
      return self.bird_id == other.bird_id and self.picture_id == other.picture_id
    return False


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
