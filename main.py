from src.interfaces.db import DB

from src.models.slack import Slack
from src.models.exercise import Exercise
from src.models.user import User

exercise = Exercise()
slack = Slack()

db = DB()
User.create("U07K8N96NDA", "abdur.rahman", "T07JYJP5M6D", -14400, "0 0 0 0 0")

print(len(User.get_all()))
# User.update("U07K8N96NDN", name="sarthak")

# print(User.get("U07K8N96NDN").name)

# User.delete("U07K8N96NDN")

db.disconnect()
# slack.send_reminder("U07K8N96NDN", exercise.get_random())