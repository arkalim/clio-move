import time
import schedule
import threading

def schedule_reminders():
  print("Reminder scheduled!")
  print(time.time())

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