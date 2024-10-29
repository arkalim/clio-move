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
  def image(url, alt_text):
    return {
      "type": "image",
      "image_url": url,
      "alt_text": alt_text
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

  @staticmethod
  def context(text):
    return {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": text
        }
      ]
    }