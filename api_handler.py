#!env/bin/python
########  imports  ##########
from flask import Flask, jsonify, request, render_template
import parse_event
# from parse_event import extract_data, schedule, onload
import json

app = Flask(__name__)

@app.route('/onload', methods = ['POST'])
def schedule_onload():
  parse_event.onload()
  return 'success'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test', methods=['POST'])
def eventsDataHandler():
	print('here')
	output = request.get_json()
	output = json.loads(output)
	print(output)

	output = parse_event.extract_data(output['data'])
	print("OUT:", output)
	return jsonify(output)

@app.route('/schedule', methods = ['POST'])
def scheduleHandler():
  print('AMALHASARRIVED')
  parse_event.schedule()
  return 'SUCCESS'


if __name__== "__main__":
	app.run(debug=True, port=9003)

