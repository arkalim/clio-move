from src.interfaces.slack import SlackInterface
from src.models.user import User
from src.utils.slack import SlackBlock

class Slack:
  def __init__(self):
    self.slack_interface = SlackInterface()

  def construct_reminder(self, exercise):
    steps_text = "\n".join(f"• {step}" for step in exercise["steps"])
    blocks = [
      SlackBlock.text(f"Time to take a break and perform *{exercise['name']}*. {exercise['description']}"),
      SlackBlock.text(f"*Steps:*\n{steps_text}"),
      SlackBlock.image(exercise["image_url"], exercise["name"]),
      SlackBlock.context(exercise["image_credit"])
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

  def enable_user(self, user_id):
    if User.exists(user_id):
      return False

    user = self.slack_interface.get_user_info(user_id)["user"]
    if user["is_bot"]:
      return False
    
    User.create(
      id=user["id"], 
      name=user["name"], 
      tz_offset=user["tz_offset"],
    )
    return True

  def disable_user(self, user_id):
    if not User.exists(user_id):
      return False
    User.delete(user_id)
    return True

  def load_home_tab(self, user_id):
    self.slack_interface.publish_view(user_id, self.construct_home_tab(User.exists(user_id)))

  def handle_command(self, data):
    command = data["text"]
    message = "Unsupported command!!!"
    return self.construct_reply(message)

  def handle_event(self, data):
    event_category = data["type"]

    if event_category == "url_verification":
      return { "challenge": data["challenge"] }

    elif event_category == "event_callback":
      event_type = data["event"]["type"]

      if event_type == "app_home_opened":
        user_id = data["event"]["user"]
        self.load_home_tab(user_id)

  def handle_interaction(self, data):
    user_id = data["user"]["id"]
    actions = data["actions"]

    for action in actions:
      action_id = action["action_id"]

      if action_id == "enable":
        if self.enable_user(user_id):
          self.load_home_tab(user_id)

      elif action_id == "disable":
        if self.disable_user(user_id):
          self.load_home_tab(user_id)

  
  def construct_home_tab(self, enabled):
    if enabled:
      return {
        "type": "home",
        "blocks": [
          SlackBlock.text("*Welcome to Clio Move!* :wave:\n You're all set! This app will send periodic reminders every hour to stretch, walk, or do quick exercises throughout your workday."),
          SlackBlock.divider(),
          SlackBlock.text("If you're not enjoying the app, feel free to disable it using the button below."),
          SlackBlock.actions([
            SlackBlock.button("Disable", "disable", "danger")
          ])
        ]
      }

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