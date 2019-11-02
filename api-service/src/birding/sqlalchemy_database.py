from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class EngineFactory:

  def create_engine(self, host: str, dbname: str, user: str,
        password: str) -> Engine:
    url = f'postgresql+psycopg2://{user}:{password}@{host}/{dbname}'
    return create_engine(url, echo=True)


class BaseFactory:

  def create_base(self):
    return declarative_base()


class SessionFactory:

  def __init__(self, engine: Engine):
    self.engine = engine

  def create_session(self) -> Session:
    session_class = sessionmaker(bind=self.engine)
    return session_class()

Base = BaseFactory().create_base()