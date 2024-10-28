import json

class Exercise:
  def __init__(self):
    self.exercises = json.load(open("data/exercises.json"))

  def get_random(self):
    return self.exercises[0]