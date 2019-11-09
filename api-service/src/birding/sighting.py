from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from .v0.models import Sighting


class SightingRepository:

  def __init__(self, sqlalchemy_session: Session) -> None:
    self.session = sqlalchemy_session

  def find_sighting(self, sighting_id: int) -> Optional[Sighting]:
    return self.session.query(Sighting).get(sighting_id)

  def delete_sighting(self, sighting_id: int) -> bool:
    count = self.session.query(Sighting).filter_by(id=sighting_id).delete()
    self.session.commit()
    return count == 1

  def add_sighting(self, sighting: Sighting) -> Optional[Sighting]:
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
