import psycopg2
from retrying import retry

class DatabaseConnector:

  @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
  def connect(host, dbname, user, password):
    kwargs = {'host': host, 'dbname': dbname, 'user': user, 'password': password}
    connection = psycopg2.connect(**kwargs)
    return Database(connection)

class Database:

  def __init__(self, connection):
    self.connection = connection

  def fetchone(self, query, vars=None):
    result = self.query(query, vars)
    if result:
      return result[0]
    else:
      return None

  def query(self, query, vars=None):
    cursor = self.connection.cursor()
    cursor.execute(query, vars)
    result = None
    try:
      result = cursor.fetchall()
    except:
      pass
    self.connection.commit()
    cursor.close()
    return result
