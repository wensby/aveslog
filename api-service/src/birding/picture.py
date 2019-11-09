from sqlalchemy.orm import Session
from .v0.models import Picture


class PictureRepository:

  def __init__(self, sqlalchemy_session: Session):
    self.session = sqlalchemy_session

  def pictures(self):
    return self.session.query(Picture).all()
