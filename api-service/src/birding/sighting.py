from datetime import date, time
from typing import Optional, Any

from .database import Database


class SightingPost:

  def __init__(self, person_id, bird_id, date, time=None):
    self.person_id = person_id
    self.bird_id = bird_id
    self.date = date
    self.time = time


class Sighting:

  def __init__(self,
        id: int,
        person_id: int,
        bird_id: int,
        sighting_date: date,
        sighting_time: Optional[time]) -> None:
    self.id: int = id
    self.person_id: int = person_id
    self.bird_id: int = bird_id
    self.sighting_date: date = sighting_date
    self.sighting_time: Optional[time] = sighting_time

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, Sighting):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self) -> str:
    return (f'{self.__class__.__name__}({self.id}, {self.person_id}, '
            f'{self.bird_id}, {self.sighting_date}, {self.sighting_time})')


class SightingRepository:

  def __init__(self, database: Database) -> None:
    self.database: Database = database

  def find_sighting(self, sighting_id: int) -> Optional[Sighting]:
    query = ('SELECT id, person_id, bird_id, sighting_date, sighting_time '
             'FROM sighting '
             'WHERE id = %s;')
    result = self.database.query(query, (sighting_id,))
    return next(map(self.sighting_from_row, result.rows), None)

  def delete_sighting(self, sighting_id: int) -> bool:
    query = ('DELETE '
             'FROM sighting '
             'WHERE id = %s;')
    result = self.database.query(query, (sighting_id,))
    return 'DELETE' in result.status

  def sighting_from_row(self, row: list) -> Sighting:
    return Sighting(row[0], row[1], row[2], row[3], row[4])

  def add_sighting(self, sighting_post: SightingPost) -> bool:
    query = (
      'INSERT INTO '
      '  sighting (person_id, bird_id, sighting_date, sighting_time) '
      'VALUES '
      '  (%s, %s, %s, %s);'
    )
    args = (
      sighting_post.person_id,
      sighting_post.bird_id,
      sighting_post.date,
      sighting_post.time,
    )
    result = self.database.query(query, args)
    return 'INSERT 0 1' in result.status
