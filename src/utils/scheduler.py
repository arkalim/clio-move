import time
import schedule
import threading
from datetime import datetime, timedelta

from src.models.user import User
from src.models.slack import Slack
from src.models.exercise import Exercise

slack = Slack()

START_WORK_HOUR = 9
END_WORK_HOUR = 17

def schedule_reminders():
  try:
    exercise = Exercise.get_random()
    print(f"Scheduling reminders for exercise: {exercise["name"]}")
    for user in User.get_all():
      try:
        current_time = datetime.utcfromtimestamp(int(time.time()) + user.tz_offset)
        if START_WORK_HOUR <= current_time.hour < END_WORK_HOUR:
          slack.send_reminder(user.id, exercise)
          print(f"Sent reminder to {user.name} at local time {current_time}")
          time.sleep(1)
      except:
        print(f"Failed to schedule reminder to {user.name} at local time {current_time}")
  except Exception as e:
    print(f"Failed to schedule reminders for exercise: {exercise["name"]}")

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