from typing import Any

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography

Base = declarative_base()


class BirdThumbnail(Base):
  __tablename__ = 'bird_thumbnail'
  bird_id = Column(Integer, ForeignKey('bird.id'), primary_key=True)
  picture_id = Column(Integer, ForeignKey('picture.id'))
  bird = relationship('Bird', back_populates='thumbnail')
  picture = relationship('Picture')

  def __repr__(self) -> str:
    return \
      f"<BirdThumbnail(bird_id='{self.bird_id}', picture_id='{self.picture_id}')>"

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, BirdThumbnail):
      return self.bird_id == other.bird_id and self.picture_id == other.picture_id
    return False


class Bird(Base):
  __tablename__ = 'bird'
  id = Column(Integer, primary_key=True)
  binomial_name = Column(String, nullable=False)
  common_names = relationship('BirdCommonName')
  thumbnail: BirdThumbnail = relationship('BirdThumbnail', uselist=False)
  looks = relationship('BirdLook')

  def __eq__(self, other: Any):
    if isinstance(other, Bird):
      return self.id == other.id and self.binomial_name == other.binomial_name
    return False

  def __repr__(self):
    return f"<Bird(binomial_name='{self.binomial_name}')>"

  def __hash__(self) -> int:
    return hash((self.id, self.binomial_name))


class Locale(Base):
  __tablename__ = 'locale'
  id = Column(Integer, primary_key=True)
  code = Column(String, nullable=False)

  def __repr__(self) -> str:
    return f"<Locale(code='{self.code}')>"

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, self.__class__):
      return self.id == other.id and self.code == other.code
    return False


class BirdCommonName(Base):
  __tablename__ = 'bird_common_name'
  id = Column(Integer, primary_key=True)
  bird_id = Column(Integer, ForeignKey('bird.id'), nullable=False)
  locale_id = Column(Integer, ForeignKey('locale.id'), nullable=False)
  name = Column(String, nullable=False)
  bird = relationship('Bird', uselist=False)
  locale = relationship('Locale', uselist=False, lazy='joined')

  def __repr__(self) -> str:
    return f"<BirdCommonName(name='{self.name}')>"


class BirderConnection(Base):
  __tablename__ = 'birder_connection'
  id = Column(Integer, primary_key=True)
  primary_birder_id = Column(Integer, ForeignKey('birder.id'))
  secondary_birder_id = Column(Integer, ForeignKey('birder.id'))
  modification_datetime = Column(
    DateTime, nullable=False, default=func.current_timestamp()
  )
  __table_args__ = (UniqueConstraint(
    'primary_birder_id',
    'secondary_birder_id',
    name='birder_connection_birder_ids_unique'),
  )

  connection_birder = relationship(
    'Birder', uselist=False, foreign_keys=[secondary_birder_id],
  )


class Birder(Base):
  __tablename__ = 'birder'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  sightings = relationship('Sighting')
  connections = relationship(
    'BirderConnection', foreign_keys='BirderConnection.primary_birder_id',
  )

  def __repr__(self):
    return f"<Birder(name='{self.name}')>"


class HashedPassword(Base):
  __tablename__ = 'hashed_password'
  account_id = Column(Integer, ForeignKey('account.id'), primary_key=True)
  salt = Column(String, nullable=False)
  salted_hash = Column(String, nullable=False)


account_role_table = Table('account_role', Base.metadata,
  Column('account_id', Integer, ForeignKey('account.id'), nullable=False),
  Column('role_id', Integer, ForeignKey('role.id'), nullable=False))

role_resource_permission_table = Table('role_resource_permission',
  Base.metadata,
  Column('role_id', Integer, ForeignKey('role.id'), nullable=False),
  Column(
    'resource_permission_id', Integer, ForeignKey(
      'resource_permission.id'
    ), nullable=False
  ))


class Account(Base):
  __tablename__ = 'account'
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  email = Column(String, nullable=False)
  birder_id = Column(Integer, ForeignKey('birder.id'))
  locale_id = Column(Integer, nullable=True)
  creation_datetime = Column(
    DateTime, nullable=False, default=func.current_timestamp()
  )

  birder: Birder = relationship('Birder', uselist=False)
  refresh_tokens = relationship('RefreshToken', back_populates='account')
  hashed_password: HashedPassword = relationship('HashedPassword',
    uselist=False)
  password_reset_token = relationship('PasswordResetToken', uselist=False)
  roles = relationship(
    'Role', secondary=account_role_table, back_populates='accounts'
  )

  def __repr__(self):
    return (f"<Account(username='{self.username}', email='{self.email}', "
            f"birder_id='{self.birder_id}', locale_id='{self.locale_id}')>")


class Role(Base):
  __tablename__ = 'role'
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)

  accounts = relationship(
    'Account', secondary=account_role_table, back_populates='roles'
  )
  resource_permissions = relationship(
    'ResourcePermission',
    secondary=role_resource_permission_table,
    back_populates='roles'
  )


class ResourcePermission(Base):
  __tablename__ = 'resource_permission'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  resource_regex = Column(String, nullable=False)
  method = Column(String, nullable=False)

  roles = relationship(
    'Role',
    secondary=role_resource_permission_table,
    back_populates='resource_permissions'
  )

  def __repr__(self):
    return f'ResourcePermission<name={self.name}, resource_regex={self.resource_regex}, method={self.method}>'


class RegistrationRequest(Base):
  __tablename__ = 'registration_request'
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False)
  token = Column(String, nullable=False)


class PasswordResetToken(Base):
  __tablename__ = 'password_reset_token'
  account_id = Column(Integer, ForeignKey('account.id'), primary_key=True)
  token = Column(String)

  account = relationship('Account', uselist=False)

  def __repr__(self):
    return (
      f"<PasswordResetToken(account_id='{self.account_id}', "
      f"token='{self.token}')>"
    )

  def __eq__(self, other):
    if isinstance(other, PasswordResetToken):
      return (
            self.account_id == other.account_id and
            self.token == other.token
      )
    return False


class Picture(Base):
  __tablename__ = 'picture'
  id = Column(Integer, primary_key=True)
  filepath = Column(String)
  credit = Column(String)

  def __repr__(self):
    return f"<Picture(filepath='{self.filepath}', credit='{self.credit}')>"


class Sighting(Base):
  __tablename__ = 'sighting'
  id = Column(Integer, primary_key=True)
  birder_id = Column(Integer, ForeignKey('birder.id'))
  bird_id = Column(Integer, ForeignKey('bird.id'))
  sighting_date = Column(Date, nullable=False)
  sighting_time = Column(Time)
  position_id = Column(Integer, ForeignKey('position.id'))
  bird = relationship('Bird')
  position = relationship('Position', uselist=False)

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


class Position(Base):
  __tablename__ = 'position'
  id = Column(Integer, primary_key=True)
  point = Column(Geography('POINT', 4326), nullable=False)
  names = relationship('PositionName')


class PositionName(Base):
  __tablename__ = 'position_name'
  id = Column(Integer, primary_key=True)
  position_id = Column(Integer, ForeignKey('position.id'), nullable=False)
  locale_id = Column(Integer, ForeignKey('locale.id'), nullable=False)
  detail_level = Column(Integer)
  name = Column(String, nullable=False)
  creation_time = Column(DateTime, nullable=False)
  locale = relationship('Locale', uselist=False)


class RefreshToken(Base):
  __tablename__ = 'refresh_token'
  id = Column(Integer, primary_key=True)
  token = Column(String, nullable=False)
  account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
  expiration_date = Column(DateTime, nullable=False)
  account = relationship('Account', back_populates='refresh_tokens')


class BirdLook(Base):
  __tablename__ = 'bird_look'
  id = Column(Integer, primary_key=True)
  bird_id = Column(Integer, ForeignKey('bird.id'), nullable=False)
  label = Column(String)
  description = Column(String)
