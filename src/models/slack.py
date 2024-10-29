from src.interfaces.slack import SlackInterface
from src.models.user import User

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

  def send_reminder(self, channel, exercise):
    return self.slack_interface.send_message(channel, self.construct_reminder(exercise))

  def schedule_reminder(self, channel, exercise, time):
    return self.slack_interface.schedule_message(channel, self.construct_reminder(exercise), int(time))

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
        interval=45
      )
      return self.construct_reply("Clio Move enabled!")

    elif command == "disable":
      user_id = data["user_id"]

      if not User.exists(user_id):
        return self.construct_reply("Clio Move is already disabled for you.")

      User.delete(user_id)
      return self.construct_reply("Clio Move disabled!")

    return self.construct_reply(message)