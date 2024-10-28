from src.models.slack import Slack
from src.models.exercise import Exercise

exercise = Exercise()
slack = Slack()

slack.send_reminder("U07K8N96NDN", exercise.get_random())