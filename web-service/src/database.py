import psycopg2

class Database:

  def __init__(self, host, dbname, user, password):
    kwargs = {'host': host, 'dbname': dbname, 'user': user, 'password': password}
    self.connection = psycopg2.connect(**kwargs)

  def fetchone(self, query, vars=None):
    result = self.doquery(query, vars)
    if result:
      return result[0]
    else:
      return None

  def doquery(self, query, vars=None):
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
