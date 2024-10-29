import threading
from src.utils.scheduler import start_scheduler_thread
from src.utils.api import app

if __name__ == "__main__":
  start_scheduler_thread()
  app.run(debug=True, use_reloader=False, port=8000, host="0.0.0.0")