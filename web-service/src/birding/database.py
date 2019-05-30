import psycopg2
from retrying import retry

class DatabaseConnectionFactory:

  def __init__(self, logger):
    self.logger = logger

  def create_connection(self, host, dbname, user, password):
    connection = self.connect(host, dbname, user, password)
    self.logger.info('Database connection established')
    return Database(connection)

  @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
  def connect(self, host, dbname, user, password):
    kwargs = {
        'host': host,
        'dbname': dbname,
        'user': user,
        'password': password
    }
    self.logger.info('Connecting to database ' + dbname)
    return psycopg2.connect(**kwargs)

class Database:

  def __init__(self, connection):
    self.connection = connection

  def query(self, query, vars=None):
    cursor = self.connection.cursor()
    cursor.execute(query, vars)
    try:
      result = cursor.fetchall()
    except:
      result = None
    self.connection.commit()
    cursor.close()
    return result
