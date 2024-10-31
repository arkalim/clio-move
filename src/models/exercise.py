import json
import random

class Exercise:
  exercises = json.load(open("data/exercises.json"))

  @classmethod
  def generate(cls):
    while True:
      sequence = cls.exercises.copy()
      random.shuffle(sequence)
      for exercise in sequence:
        yield exercise