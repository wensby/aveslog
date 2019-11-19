from typing import Optional

from flask import g

from aveslog.v0.models import Birder


class BirderRepository:

  def add_birder(self, name):
    g.database_session.rollback()
    birder = Birder(name=name)
    g.database_session.add(birder)
    g.database_session.commit()
    return birder

  def birder_by_id(self, birder_id: int) -> Optional[Birder]:
    return g.database_session.query(Birder).get(birder_id)
