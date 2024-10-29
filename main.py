import json
import threading
from flask import Flask, jsonify, request

from src.utils.scheduler import start_scheduler_thread
from src.interfaces.db import DB
from src.models.slack import Slack

app = Flask("Clio Move")

slack = Slack()
db = DB()

@app.teardown_appcontext
def close_db(exception=None):
  db.disconnect()

@app.route('/command', methods=['POST'])
def command():
  response = slack.handle_command(request.form)
  return jsonify(response)

@app.route('/event', methods=['POST'])
def event():
  response = slack.handle_event(request.get_json())
  return jsonify(response) if response else jsonify({"status": "ok"})

@app.route('/interaction', methods=['POST'])
def interaction():
  payload = json.loads(request.form.get("payload"))
  response = slack.handle_interaction(payload)
  return jsonify(response) if response else jsonify({"status": "ok"})

if __name__ == "__main__":
  start_scheduler_thread()
  app.run(debug=True, use_reloader=False, port=8000, host="0.0.0.0")