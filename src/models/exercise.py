import json
import random

class Exercise:
  exercises = json.load(open("data/exercises.json"))

  @classmethod
  def get_random(self):
    return random.choice(cls.exercises)