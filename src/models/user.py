from datetime import datetime, timedelta
from schema.user import User as UserModel
from peewee import SqliteDatabase, Model, CharField, IntegerField

class User:
  @staticmethod
  def create(id, name, tz_offset, interval):
    if UserModel.select().where(UserModel.id == id).exists():
      return None
    return UserModel.create(
      id=id,
      name=name,
      tz_offset=tz_offset,
      interval=interval,
      next_reminder_at=datetime.now() + timedelta(minutes=interval)
    )

  @staticmethod
  def get_all():
    return UserModel.select()

  @staticmethod
  def get(id):
    return UserModel.get(UserModel.id == id)

  @staticmethod
  def update(id, **kwargs):
    return UserModel.update(**kwargs).where(UserModel.id == id).execute()

  @staticmethod
  def delete(id):
    return UserModel.delete().where(UserModel.id == id).execute()