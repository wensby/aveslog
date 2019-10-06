from typing import Any, Type, TypeVar, Optional, List

from .database import Database


class Bird:

  def __init__(self, bird_id: int, binomial_name: str) -> None:
    self.id: int = bird_id
    self.binomial_name: str = binomial_name

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, Bird):
      return self.__dict__ == other.__dict__
    return False

  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self.id}, {self.binomial_name})'

  def __hash__(self) -> int:
    return hash((self.id, self.binomial_name))


T = TypeVar('T', bound='BirdThumbnail')


class BirdThumbnail:

  def __init__(self, bird_id: int, picture_id: int) -> None:
    self.bird_id: int = bird_id
    self.picture_id: int = picture_id

  @classmethod
  def fromrow(cls: Type[T], row: list) -> T:
    return cls(row[0], row[1])

  def __repr__(self) -> str:
    return \
      f'BirdThumbnail<bird_id={self.bird_id}, picture_id={self.picture_id}>'

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, BirdThumbnail):
      return self.__dict__ == other.__dict__
    return False


class BirdRepository:

  def __init__(self, database: Database) -> None:
    self.database: Database = database

  def fetchonebird(self,
        query: str,
        vars: Optional[tuple] = None) -> Optional[Bird]:
    result = self.database.query(query, vars)
    if len(result.rows) == 1:
      return self.bird_from_row(result.rows[0])

  def bird_thumbnail(self, bird: Bird) -> Optional[BirdThumbnail]:
    query = (
      'SELECT bird_id, picture_id '
      'FROM bird_thumbnail '
      'WHERE bird_id = %s;'
    )
    result = self.database.query(query, (bird.id,))
    return next(map(BirdThumbnail.fromrow, result.rows), None)

  def bird_from_row(self, row: list) -> Bird:
    return Bird(row[0], row[1])

  def get_bird_by_id(self, id: int) -> Optional[Bird]:
    return self.fetchonebird(
      "SELECT id, binomial_name FROM bird WHERE id = %s;", (id,))

  def get_bird_by_binomial_name(self, binomial_name: str) -> Optional[Bird]:
    return self.fetchonebird(
      "SELECT id, binomial_name FROM bird WHERE binomial_name ILIKE %s;",
      (binomial_name,))

  @property
  def birds(self) -> List[Bird]:
    result = self.database.query("SELECT * FROM bird;")
    birds = []
    for row in result.rows:
      bird = Bird(row[0], row[1])
      birds.append(bird)
    return birds
