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
          SlackBlock.text(":wave: *Welcome to Clio Move*"),
          SlackBlock.text("You're all set to receive hourly reminders during your work hours to take a break, stretch, and keep your body happy. Each reminder comes with easy-to-follow steps and a quick gif so you can follow along."),
          SlackBlock.divider(),
          SlackBlock.text("If you wish to not receive further reminders, feel free to disable the app!"),
          SlackBlock.actions([
            SlackBlock.button("Disable", "disable", "danger")
          ])
        ]
      }

    return {
      "type": "home",
      "blocks": [
        SlackBlock.text(":wave: *Welcome to Clio Move*"),
        SlackBlock.text("We all know how easy it is to stay glued to the screen for hours 🧑🏽‍💻, but taking regular breaks and moving is crucial. Staying active while working improves circulation, reduces stress, and helps prevent stiffness and fatigue from sitting all day. With Clio Move, you get gentle, hourly reminders during your work hours to take a break, stretch, and keep your body happy. Each reminder comes with easy-to-follow steps and a quick gif so you can follow along."),
        SlackBlock.text("🚀 Stay focused, stay healthy, and let Clio Move bring balance to your workday, one stretch at a time!"),
        SlackBlock.divider(),
        SlackBlock.text("Enable the app to get started!"),
        SlackBlock.actions([
          SlackBlock.button("Enable", "enable", "primary")
        ])
      ]
    }