from psycopg2.pool import SimpleConnectionPool
from retrying import retry


def read_script_file(filename: str) -> str:
  with open(f'birding/resources/{filename}', 'r') as file:
    return file.read()


class DatabaseFactory:

  def __init__(self, logger):
    self.logger = logger

  def create_database(self, host, dbname, user, password):
    pool = SimpleConnectionPool(1, 20, user=user, password=password, host=host,
                                database=dbname)
    self.logger.info(f'Database ({dbname}) connection pool created')
    return Database(self.logger, pool)


class Database:

  def __init__(self, logger, connection_pool):
    self.logger = logger
    self.connection_pool = connection_pool

  def transaction(self):
    return Transaction(self.connection_pool)

  def query(self, query, vars=None):
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


class Transaction:

  def __init__(self, connection_pool):
    self.connection_pool = connection_pool

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

  def execute(self, query, vars=None, mapper=None):
    self.cursor.execute(query, vars)
    try:
      rows = self.cursor.fetchall()
    except:
      rows = []
    status = self.cursor.statusmessage
    if mapper:
      rows = list(map(mapper, rows))
    return QueryResult(status, rows)


class QueryResult:

  def __init__(self, status, rows):
    self.status = status
    self.rows = rows
