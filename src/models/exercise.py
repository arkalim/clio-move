import json
import random

from src.utils.logger import logger

class Exercise:
  exercises = json.load(open("data/exercises.json"))
  logger.info(f"Found {len(exercises)} exercises.")

  @classmethod
  def generate(cls):
    while True:
      sequence = cls.exercises.copy()
      random.shuffle(sequence)
      for exercise in sequence:
        yield exercise