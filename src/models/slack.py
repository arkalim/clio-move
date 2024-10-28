from src.interfaces.slack import SlackInterface

class Slack:
  def __init__(self):
    self.slack_interface = SlackInterface()

  def send_reminder(self, channel, exercise):
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
    return self.slack_interface.send_message(channel, blocks)