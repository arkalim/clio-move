from datetime import datetime, timedelta
from schema.user import User as UserModel

class User:
  @classmethod
  def create(cls, id, name, tz_offset):
    if cls.exists(id):
      return None
    return UserModel.create(
      id=id,
      name=name,
      tz_offset=tz_offset,
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
  def update(id, **kwargs):
    return UserModel.update(**kwargs).where(UserModel.id == id).execute()

  @staticmethod
  def delete(id):
    return UserModel.delete().where(UserModel.id == id).execute()