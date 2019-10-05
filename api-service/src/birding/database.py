from logging import Logger
from typing import Callable, Any

from psycopg2.pool import SimpleConnectionPool
from retrying import retry


def read_script_file(filename: str) -> str:
  with open(f'birding/resources/{filename}', 'r') as file:
    return file.read()


class QueryResult:

  def __init__(self, status: str, rows: list) -> None:
    self.status: str = status
    self.rows: rows = rows


class Transaction:

  def __init__(self, connection_pool: SimpleConnectionPool) -> None:
    self.connection_pool: SimpleConnectionPool = connection_pool

  def __enter__(self):
    self.connection = self.__get_connection()
    self.cursor = self.connection.cursor()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.connection.commit()
    self.cursor.close()
    self.connection_pool.putconn(self.connection)

  @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
  def __get_connection(self):
    return self.connection_pool.getconn()

  def execute(self,
        query: str,
        vars: tuple = None,
        mapper: Callable[[list], Any] = None) -> QueryResult:
    self.cursor.execute(query, vars)
    try:
      rows = self.cursor.fetchall()
    except:
      rows = []
    status = self.cursor.statusmessage
    if mapper:
      rows = list(map(mapper, rows))
    return QueryResult(status, rows)


class Database:

  def __init__(self,
        logger: Logger,
        connection_pool: SimpleConnectionPool) -> None:
    self.logger: Logger = logger
    self.connection_pool: SimpleConnectionPool = connection_pool

  def transaction(self) -> Transaction:
    return Transaction(self.connection_pool)

  def query(self, query: str, vars: tuple = None) -> QueryResult:
    connection = self.__get_connection()
    cursor = connection.cursor()
    cursor.execute(query, vars)
    try:
      rows = cursor.fetchall()
    except:
      rows = []
    status = cursor.statusmessage
    result = QueryResult(status, rows)
    connection.commit()
    cursor.close()
    self.logger.info('Releasing database connection')
    self.connection_pool.putconn(connection)
    return result

  @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
  def __get_connection(self):
    self.logger.info('Getting database connection')
    return self.connection_pool.getconn()


class DatabaseFactory:

  def __init__(self, logger: Logger) -> None:
    self.logger: Logger = logger

  def create_database(self,
        host: str,
        dbname: str,
        user: str,
        password: str) -> Database:
    pool = SimpleConnectionPool(1, 20, user=user, password=password, host=host,
                                database=dbname)
    self.logger.info(f'Database ({dbname}) connection pool created')
    return Database(self.logger, pool)
