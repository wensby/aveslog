from typing import Any, Type, TypeVar, Optional, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from .database import Database
from .sqlalchemy_database import Base


class Bird(Base):
  __tablename__ = 'bird'
  id = Column(Integer, primary_key=True)
  binomial_name = Column(String, nullable=False)

  def __eq__(self, other: Any):
    if isinstance(other, Bird):
      return self.id == other.id and self.binomial_name == other.binomial_name
    return False

  def __repr__(self):
    return f"<Bird(binomial_name='{self.binomial_name}')>"

  def __hash__(self) -> int:
    return hash((self.id, self.binomial_name))


T = TypeVar('T', bound='BirdThumbnail')


class BirdThumbnail:

  def __init__(self, bird_id: int, picture_id: int) -> None:
    self.bird_id: int = bird_id
    self.picture_id: int = picture_id

  @classmethod
  def fromrow(cls: Type[T], row: list) -> T:
    return cls(row[0], row[1])

  def __repr__(self) -> str:
    return \
      f'BirdThumbnail<bird_id={self.bird_id}, picture_id={self.picture_id}>'

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, BirdThumbnail):
      return self.__dict__ == other.__dict__
    return False


class BirdRepository:

  def __init__(self, database: Database, sqlalchemy_session: Session):
    self.database = database
    self.session = sqlalchemy_session

  def bird_thumbnail(self, bird: Bird) -> Optional[BirdThumbnail]:
    query = (
      'SELECT bird_id, picture_id '
      'FROM bird_thumbnail '
      'WHERE bird_id = %s;'
    )
    result = self.database.query(query, (bird.id,))
    return next(map(BirdThumbnail.fromrow, result.rows), None)

  def get_bird_by_id(self, id: int) -> Optional[Bird]:
    return self.session.query(Bird).get(id)

  def get_bird_by_binomial_name(self, binomial_name: str) -> Optional[Bird]:
    return self.session.query(Bird).filter(
      Bird.binomial_name.ilike(binomial_name)).first()

  @property
  def birds(self) -> List[Bird]:
    return self.session.query(Bird).all()
