from src.interfaces.slack import SlackInterface

class Slack:
  def __init__(self):
    self.slack_interface = SlackInterface()

  def send_reminder(self, channel, exercise):
    blocks = [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": exercise["name"],
        }
      },
      {
        "type": "image",
        "image_url": exercise["image_url"],
        "alt_text": exercise["name"]
      }
    ]
    return self.slack_interface.send_message(channel, blocks)