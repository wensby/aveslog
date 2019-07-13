class Picture:

  def __init__(self, id, filepath, credit):
    self.id = id
    self.filepath = filepath
    self.credit = credit

  @classmethod
  def fromrow(cls, row):
    return cls(row[0], row[1], row[2])


class PictureRepository:

  def __init__(self, database):
    self.database = database

  def pictures(self):
    result = self.database.query('SELECT id, filepath, credit FROM picture;')
    return list(map(Picture.fromrow, result.rows))
