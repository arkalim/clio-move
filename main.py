import os
from dotenv import load_dotenv

from src.interfaces.slack import Slack

load_dotenv()

slack = Slack(os.getenv("SLACK_BOT_TOKEN"))

users = slack.get_users()

for user in users:
  result = slack.send_message(user["id"],f"Hello, @{user['name']}!")