from datetime import date, time
from typing import Optional, Any, List

from .database import Database, read_script_file


class SightingPost:

  def __init__(self,
        person_id: int,
        bird_id: int,
        sighting_date: date,
        sighting_time: Optional[time] = None) -> None:
    self.person_id: int = person_id
    self.bird_id: int = bird_id
    self.date: date = sighting_date
    self.time: Optional[time] = sighting_time


class Sighting:

  @classmethod
  def fromrow(cls, row: list):
    return cls(row[0], row[1], row[2], row[3], row[4])

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

  def add_sighting(self, sighting_post: SightingPost) -> Optional[Sighting]:
    with self.database.transaction() as transaction:
      result = transaction.execute(
        'INSERT INTO sighting '
        '(person_id, bird_id, sighting_date, sighting_time) '
        'VALUES (%s, %s, %s, %s) '
        'RETURNING id, person_id, bird_id, sighting_date, sighting_time;'
        , (
          sighting_post.person_id,
          sighting_post.bird_id,
          sighting_post.date,
          sighting_post.time
        ), Sighting.fromrow)
      if not result.rows:
        return None
      else:
        return result.rows[0]

  def sightings(self, person_id: int) -> List[Sighting]:
    with self.database.transaction() as transaction:
      query = read_script_file('select_sighting_item_data.sql')
      return transaction.execute(query, (person_id,), Sighting.fromrow).rows
