from sqlalchemy.orm import Session
from .sqlalchemy_database import Base
from sqlalchemy import Column, Integer, String


class Picture(Base):
  __tablename__ = 'picture'
  id = Column(Integer, primary_key=True)
  filepath = Column(String)
  credit = Column(String)

  def __repr__(self):
    return f"<Picture(filepath='{self.filepath}', credit='{self.credit}')>"


class PictureRepository:

  def __init__(self, sqlalchemy_session: Session):
    self.session = sqlalchemy_session

  def pictures(self):
    return self.session.query(Picture).all()
