from schema.base import BaseModel as Model
from peewee import CharField, IntegerField

class User(Model):
    id = CharField(primary_key=True)
    name = CharField()
    team_id = CharField()
    tz_offset = IntegerField()
    schedule = CharField()