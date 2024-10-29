import time
import schedule
import threading
from datetime import timedelta

from src.models.user import User
from src.models.slack import Slack
from src.models.exercise import Exercise

slack = Slack()

def schedule_reminders():
  for user in User.get_expired():
    exercise = Exercise.get_random()
    next_reminder_at = user.next_reminder_at + timedelta(user.interval)
    slack.schedule_reminder(user.id, exercise, next_reminder_at)
    User.update(user.id, next_reminder_at=next_reminder_at)
    time.sleep(2)

def run_scheduler():
  schedule.every(10).seconds.do(schedule_reminders)
  while True:
    schedule.run_pending()
    time.sleep(1)

def start_scheduler_thread():
  if not any(thread.name == "SchedulerThread" for thread in threading.enumerate()):
    scheduler_thread = threading.Thread(target=run_scheduler, name="SchedulerThread")
    scheduler_thread.daemon = True
    scheduler_thread.start()