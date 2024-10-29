from src.interfaces.db import DB

from src.models.slack import Slack
from src.models.exercise import Exercise
from src.models.user import User

from flask import Flask, jsonify, request

app = Flask("Clio Move")

exercise = Exercise()
slack = Slack()
db = DB()

@app.teardown_appcontext
def close_db(exception=None):
  db.disconnect()

@app.route('/')
def home():
  print("Hello")
  return "Hello, welcome to the API!"

@app.route('/command', methods=['POST'])
def command():
  response = slack.handle_command(request.form)
  return jsonify(response)

app.run(debug=True, port=8000, host="0.0.0.0")