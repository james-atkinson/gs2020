from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from SimConnect import *
from time import sleep
import random
import sys

app = Flask(__name__)
CORS(app)

# SimConnect connection variables
sm = None
ae = None
aq = None

# Requestable DataSets
request_uidata = [
	'SIM_ON_GROUND',
	'PUSHBACK_STATE',
	'JETWAY_MOVING',
	'FUELTRUCK_HOSE_DEPLOYED',
	'GROUND_VELOCITY',
	'BRAKE_PARKING_POSITION',
	'WISKEY_COMPASS_INDICATION_DEGREES',
	'MAGVAR',
	'PUSHBACK_AVAILABLE',
]

# Internal functions
def get_dataset(data_type):
	if data_type == "uidata": request_to_action = request_uidata

	return request_to_action

def get_datapoint(datapoint_name, index=None):
	# This function actually does the work of getting the datapoint

	if index is not None and ':index' in datapoint_name:
		dp = aq.find(datapoint_name)
		if dp is not None:
			dp.setIndex(int(index))

	return aq.get(datapoint_name)

def set_datapoint(datapoint_name, index=None, value_to_use=None):
	# This function actually does the work of setting the datapoint

	if index is not None and ':index' in datapoint_name:
		clas = aq.find(datapoint_name)
		if clas is not None:
			clas.setIndex(int(index))

	sent = False
	if value_to_use is None:
		sent = aq.set(datapoint_name, 0)
	else:
		sent = aq.set(datapoint_name, int(value_to_use))

	if sent is True:
		status = "success"
	else:
		status = "Error with sending request: %s" % (datapoint_name)

	return status

def trigger_event(event_name, value_to_use = None):
	# This function actually does the work of triggering the event

	EVENT_TO_TRIGGER = ae.find(event_name)
	if EVENT_TO_TRIGGER is not None:
		if value_to_use is None:
			EVENT_TO_TRIGGER()
		else:
			EVENT_TO_TRIGGER(int(value_to_use))

		status = "success"
	else:
		status = "Error: %s is not an Event" % (event_name)

	return status

# Routes

# Tell the server to connect to SimConnect
@app.route('/connect'):
	sm = SimConnect()
	ae = AircraftEvents(sm)
	aq = AircraftRequests(sm, _time=10)

# Default catch-all route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def glass():
	return render_template("index.html")

# Fetch a dataset
@app.route('/dataset/<dataset_name>/', methods=["GET"])
def output_json_dataset(dataset_name):
	dataset_map = {}
	data_dictionary = get_dataset(dataset_name)
	for datapoint_name in data_dictionary:
		dataset_map[datapoint_name] = aq.get(datapoint_name)
	return jsonify(dataset_map)

# Fetch a datapoint
@app.route('/datapoint/<datapoint_name>/get', methods=["GET"])
def get_datapoint_endpoint(datapoint_name):
	ds = request.get_json() if request.is_json else request.form
	index = ds.get('index')

	output = get_datapoint(datapoint_name, index)

	if isinstance(output, bytes):
		output = output.decode('ascii')

	return jsonify(output)

# Set a datapoint
@app.route('/datapoint/<datapoint_name>/set', methods=["POST"])
def set_datapoint_endpoint(datapoint_name):
	ds = request.get_json() if request.is_json else request.form
	index = ds.get('index')
	value_to_use = ds.get('value_to_use')

	status = set_datapoint (datapoint_name, index, value_to_use)

	return jsonify(status)

# Trigger an event
@app.route('/event/<event_name>/trigger', methods=["POST"])
def trigger_event_endpoint(event_name):
	ds = request.get_json() if request.is_json else request.form
	value_to_use = ds.get('value_to_use')

	print(value_to_use, file=sys.stderr)

	status = trigger_event(event_name, value_to_use)

	return jsonify(status)

app.run(host='0.0.0.0', port=5000, debug=True)