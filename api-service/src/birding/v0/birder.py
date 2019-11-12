from typing import Optional

from sqlalchemy.orm import Session

from v0.models import Birder


class BirderRepository:

  def __init__(self, sqlalchemy_session: Session):
    self.session = sqlalchemy_session

  def add_birder(self, name):
    self.session.rollback()
    birder = Birder(name=name)
    self.session.add(birder)
    self.session.commit()
    return birder

  def birder_by_id(self, birder_id: int) -> Optional[Birder]:
    return self.session.query(Birder).get(birder_id)
