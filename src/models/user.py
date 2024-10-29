from datetime import datetime, timedelta
from schema.user import User as UserModel
from peewee import SqliteDatabase, Model, CharField, IntegerField

class User:
  @classmethod
  def create(id, name, tz_offset, interval):
    if cls.exists():
      return None
    return UserModel.create(
      id=id,
      name=name,
      tz_offset=tz_offset,
      interval=interval,
      next_reminder_at=datetime.now() + timedelta(minutes=interval)
    )

  @staticmethod
  def exists(id):
    return UserModel.select().where(UserModel.id == id).exists()

  @staticmethod
  def get_all():
    return UserModel.select()

  @staticmethod
  def get(id):
    return UserModel.get(UserModel.id == id)

  @staticmethod
  def get_expired():
    return UserModel.select().where(UserModel.next_reminder_at < datetime.now())

  @staticmethod
  def update(id, **kwargs):
    return UserModel.update(**kwargs).where(UserModel.id == id).execute()

  @staticmethod
  def delete(id):
    return UserModel.delete().where(UserModel.id == id).execute()