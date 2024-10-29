class SlackBlock:

  @staticmethod
  def text(text):
    return {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": text
      }
    }

  @staticmethod
  def divider():
    return {
      "type": "divider"
    }

  @staticmethod
  def actions(elements):
    return {
      "type": "actions",
      "elements": elements
    }

  @staticmethod
  def button(label, action_id, style):
    return {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": label
      },
      "style": style,
      "action_id": action_id
    }