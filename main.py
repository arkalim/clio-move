from src.interfaces.db import DB

from src.models.slack import Slack
from src.models.exercise import Exercise
from src.models.user import User

from flask import Flask, jsonify, request

app = Flask("Clio Move")

exercise = Exercise()
slack = Slack()

db = DB()
User.create(
  id="U07K8N96NDN", 
  name="abdur.rahman", 
  tz_offset=-14400,
  interval=45
)

print(len(User.get_all()))
# User.update("U07K8N96NDN", name="sarthak")

# print(User.get("U07K8N96NDN").name)

# User.delete("U07K8N96NDN")

db.disconnect()
# slack.send_reminder("U07K8N96NDN", exercise.get_random())

@app.route('/')
def home():
  print("Hello")
  return "Hello, welcome to the API!"

@app.route('/command', methods=['POST'])
def command():

  data = request.form
  response = slack.handle_command(data)
  return jsonify(response)

app.run(debug=True, port=8000, host="0.0.0.0")