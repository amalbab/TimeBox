#!env/bin/python
########  imports  ##########
from flask import Flask, jsonify, request, render_template
from parse_event import schedule
import json

app = Flask(__name__)

@app.route('/')
def index():
	print('here')
	return render_template('index.html')

@app.route('/test', methods=['POST'])
def schedule_endpoint():
	print('here')
	output = request.get_json()
	output = json.loads(output)
	print(output)
	schedule(output['data'])
	return output

if __name__== "__main__":
	app.run(debug=True, port=9001)