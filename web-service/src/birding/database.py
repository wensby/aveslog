from psycopg2.pool import SimpleConnectionPool
from retrying import retry

class DatabaseFactory:

  def __init__(self, logger):
    self.logger = logger

  def create_database(self, host, dbname, user, password):
    pool = SimpleConnectionPool(1, 20, user=user, password=password, host=host, database=dbname)
    self.logger.info(f'Database ({dbname}) connection pool created')
    return Database(self.logger, pool)


class Database:

  def __init__(self, logger, connection_pool):
    self.logger = logger
    self.connection_pool = connection_pool

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

class QueryResult:

  def __init__(self, status, rows):
    self.status = status
    self.rows = rows
