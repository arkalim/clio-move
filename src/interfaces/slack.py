import os
from dotenv import load_dotenv
from slack_bolt import App

from src.utils.logger import logger

load_dotenv()

class SlackInterface:
  def __init__(self):
    self.app = App(token=os.getenv("SLACK_BOT_TOKEN"))

  def get_users(self):
    try:
      response = self.app.client.users_list()
      humans = [user for user in response["members"] if not user["is_bot"] and not user["id"] == "USLACKBOT"]
      active_humans = [human for human in humans if not human["deleted"]]
      filtered_humans = [{"name": user["name"], "id": user["id"], "team_id": user["team_id"]} for user in active_humans]
      return filtered_humans
    except Exception as e:
      logger.error(f"Failed to get users: {e}")
      return []

  def get_user_info(self, id):
    return self.app.client.users_info(user=id)

  def send_message(self, channel, blocks):
    return self.app.client.chat_postMessage(channel=channel, blocks=blocks)

  def schedule_message(self, channel, blocks, timestamp):
    return self.app.client.chat_scheduleMessage(channel=channel, blocks=blocks, text="", post_at=int(timestamp))

  def publish_view(self, user_id, view):
    return self.app.client.views_publish(user_id=user_id, view=view)
