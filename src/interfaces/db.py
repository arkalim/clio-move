from peewee import SqliteDatabase
from schema.user import User

class DB:
  def __init__(self):
    self.db = SqliteDatabase('db.sqlite3')
    self.db.connect()
    self.db.create_tables([User], safe=True)

  def disconnect(self):
    self.db.close()