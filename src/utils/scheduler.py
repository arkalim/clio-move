import time
import schedule
import threading
from datetime import timedelta

from src.models.user import User
from src.models.slack import Slack
from src.models.exercise import Exercise

slack = Slack()

def schedule_reminders():
  exercise = Exercise.get_random()
  print(f"Scheduling reminders for exercise: {exercise["name"]}")
  for user in User.get_all():
    slack.send_reminder(user.id, exercise)
    print(f"Sent reminder to {user.name}")
    time.sleep(1)

def run_scheduler():
  schedule.every(1).minutes.do(schedule_reminders)
  while True:
    schedule.run_pending()
    time.sleep(1)

def start_scheduler_thread():
  if not any(thread.name == "SchedulerThread" for thread in threading.enumerate()):
    scheduler_thread = threading.Thread(target=run_scheduler, name="SchedulerThread")
    scheduler_thread.daemon = True
    scheduler_thread.start()