from typing import Optional, List

from flask import g

from .models import Bird


class BirdRepository:

  def get_bird_by_binomial_name(self, binomial_name: str) -> Optional[Bird]:
    return g.database_session.query(Bird).filter(
      Bird.binomial_name.ilike(binomial_name)).first()

  @property
  def birds(self) -> List[Bird]:
    return g.database_session.query(Bird).all()
