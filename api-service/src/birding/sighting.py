from datetime import date, time
from typing import Optional, Any, List, Tuple
from sqlalchemy.orm import Session
from .sqlalchemy_database import Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Time


class SightingPost:

  def __init__(self,
        birder_id: int,
        bird_id: int,
        sighting_date: date,
        sighting_time: Optional[time] = None) -> None:
    self.birder_id: int = birder_id
    self.bird_id: int = bird_id
    self.date: date = sighting_date
    self.time: Optional[time] = sighting_time


class Sighting(Base):
  __tablename__ = 'sighting'
  id = Column(Integer, primary_key=True)
  birder_id = Column(Integer, ForeignKey('birder.id'))
  bird_id = Column(Integer, ForeignKey('bird.id'))
  sighting_date = Column(Date, nullable=False)
  sighting_time = Column(Time)

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, Sighting):
      return (self.id == other.id
              and self.birder_id == other.birder_id
              and self.bird_id == other.bird_id
              and self.sighting_date == other.sighting_date
              and self.sighting_time == other.sighting_time)
    return False

  def __repr__(self) -> str:
    return (f"<Sighting(birder_id='{self.birder_id}', "
            f"bird_id='{self.bird_id}', sighting_date='{self.sighting_date}', "
            f"sighting_time='{self.sighting_time}')>")


class SightingRepository:

  def __init__(self, sqlalchemy_session: Session) -> None:
    self.session = sqlalchemy_session

  def find_sighting(self, sighting_id: int) -> Optional[Sighting]:
    return self.session.query(Sighting).get(sighting_id)

  def delete_sighting(self, sighting_id: int) -> bool:
    count = self.session.query(Sighting).filter_by(id=sighting_id).delete()
    self.session.commit()
    return count == 1

  def add_sighting(self, sighting_post: SightingPost) -> Optional[Sighting]:
    sighting = Sighting(birder_id=sighting_post.birder_id,
                        bird_id=sighting_post.bird_id,
                        sighting_date=sighting_post.date,
                        sighting_time=sighting_post.time)
    self.session.add(sighting)
    self.session.commit()
    return sighting

  def sightings(self,
        birder_id: Optional[int] = None,
        limit: Optional[int] = None
  ) -> Tuple[List[Sighting], bool]:
    query = self.session.query(Sighting)
    if birder_id:
      query = query.filter_by(birder_id=birder_id)
    count = query.count()
    query = query.order_by(
      Sighting.sighting_date.desc(), Sighting.sighting_time.desc())
    if limit:
      query = query.limit(limit)
    return query.all(), count
