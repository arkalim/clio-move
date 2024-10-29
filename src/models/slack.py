from src.interfaces.slack import SlackInterface
from src.models.user import User
from src.utils.slack import SlackBlock

class Slack:
  def __init__(self):
    self.slack_interface = SlackInterface()

  def construct_reminder(self, exercise):
    steps_text = "\n".join(f"• {step}" for step in exercise["steps"])
    blocks = [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": f"*{exercise['name']}*\n{exercise['description']}\n\n*Steps:*\n{steps_text}",
        }
      },
      {
        "type": "image",
        "image_url": exercise["image_url"],
        "alt_text": f"{exercise["name"]} Image"
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": exercise["image_credit"]
          }
        ]
      }
    ]
    return blocks

  def send_reminder(self, user_id, exercise):
    return self.slack_interface.send_message(user_id, self.construct_reminder(exercise))

  def schedule_reminder(self, user_id, exercise, time):
    return self.slack_interface.schedule_message(user_id, self.construct_reminder(exercise), time.timestamp())

  def construct_reply(self, message, ephemeral=True):
    return {
      "response_type": "ephemeral" if ephemeral else "in_channel",
      "text": message
    }

  def handle_command(self, data):
    command = data["text"]
    message = "Unsupported command!!!"

    if command == "enable":
      user_id = data["user_id"]

      if User.exists(user_id):
        return self.construct_reply("Clio Move is already enabled for you.")

      user = self.slack_interface.get_user_info(user_id)["user"]
      if user["is_bot"]:
        return self.construct_reply("You are a bot, haha!!!")
      
      User.create(
        id=user["id"], 
        name=user["name"], 
        tz_offset=user["tz_offset"],
      )
      return self.construct_reply("Clio Move enabled!")

    elif command == "disable":
      user_id = data["user_id"]

      if not User.exists(user_id):
        return self.construct_reply("Clio Move is already disabled for you.")

      User.delete(user_id)
      return self.construct_reply("Clio Move disabled!")

    return self.construct_reply(message)

  def handle_event(self, data):
    event_category = data["type"]

    if event_category == "url_verification":
      return { "challenge": data["challenge"] }

    elif event_category == "event_callback":
      event_type = data["event"]["type"]

      if event_type == "app_home_opened":
        user_id = data["event"]["user"]
        self.slack_interface.publish_view(user_id, self.construct_home_tab(User.exists(user_id)))
  
  def construct_home_tab(self, enabled):
    return {
      "type": "home",
      "blocks": [
        SlackBlock.text("*Welcome to Clio Move!* :wave:\nEnable this app to receive periodic reminders to stretch, walk, or do quick exercises throughout your workday."),
        SlackBlock.divider(),
        SlackBlock.actions([
          SlackBlock.button("Enable", "enable", "primary")
        ])
      ]
    }