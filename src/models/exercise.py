import json

class Exercise:
  exercises = json.load(open("data/exercises.json"))

  @classmethod
  def get_random(self):
    return self.exercises[0]