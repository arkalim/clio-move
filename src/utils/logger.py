import logging
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "log"

def setup_logger():
  logger = logging.getLogger("logger")
  logger.setLevel(logging.DEBUG)

  # Rotate every midnight, keep up to 7 days of logs
  handler = TimedRotatingFileHandler(
    f"{LOG_DIR}/app.log", 
    when="midnight", 
    interval=1, 
    backupCount=7
  )
  handler.setLevel(logging.DEBUG)

  formatter = logging.Formatter(
      "%(asctime)s - %(levelname)s - %(message)s"
  )
  handler.setFormatter(formatter)

  logger.addHandler(handler)
  return logger

logger = setup_logger()
