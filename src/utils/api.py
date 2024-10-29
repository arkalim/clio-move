import json
from flask import Flask, jsonify, request
from src.models.slack import Slack
from src.interfaces.db import DB

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