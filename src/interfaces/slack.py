from slack_bolt import App

class Slack:
  def __init__(self, token):
    self.app = App(token=token)

  def get_users(self):
    try:
      response = self.app.client.users_list()
      humans = [user for user in response["members"] if not user["is_bot"] and not user["id"] == "USLACKBOT"]
      active_humans = [human for human in humans if not human["deleted"]]
      filtered_humans = [{"name": user["name"], "id": user["id"], "team_id": user["team_id"]} for user in active_humans]
      return filtered_humans
    except Exception as e:
      print(f"Failed to get users: {e}")
      return []

  def send_message(self, channel, text):
    return self.app.client.chat_postMessage(channel=channel, text=text)