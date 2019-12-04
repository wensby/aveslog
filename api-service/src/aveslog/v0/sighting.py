from typing import Optional, List, Tuple

from flask import g
from sqlalchemy.orm import joinedload
from aveslog.v0.models import Sighting


class SightingRepository:

  def sightings(self,
        birder_id: Optional[int] = None,
        limit: Optional[int] = None
  ) -> Tuple[List[Sighting], bool]:
    query = g.database_session.query(Sighting).options(joinedload('bird'))
    if birder_id:
      query = query.filter_by(birder_id=birder_id)
    count = query.count()
    query = query.order_by(
      Sighting.sighting_date.desc(), Sighting.sighting_time.desc())
    if limit:
      query = query.limit(limit)
    return query.all(), count
