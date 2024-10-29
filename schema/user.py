from schema.base import BaseModel as Model
from peewee import CharField, IntegerField, DateTimeField

class User(Model):
    id = CharField(primary_key=True)
    name = CharField(unique=True)
    tz_offset = IntegerField(default=0)