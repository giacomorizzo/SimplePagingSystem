from flask import Flask, request, url_for
import logging
import json
from SPS import exceptions
from SPS import functions

app = Flask(__name__)
app.debug = True

#TODO support multiple formats?

@app.route('/v0.1/createNotification', methods=['POST'])
def api_createNotification():
	try:
		result = functions.createNotification(request.form.get('message', None), 'dummyRequester', 'dummyReceiver')
	except exceptions.SPS_UserError as error:
		return error.message

	return json.dumps(result)

@app.route('/v0.1/getNotification/<int:notificationId>')
def api_getNotification(notificationId):
	try:
		result = functions.getNotification(notificationId) 
	except exceptions.SPS_UserError as error:
		return error.message

	return json.dumps(result)

@app.route('/v0.1/getAvailableNotifications')
def api_getAvailableNotifications():
	try:
		result = functions.getAvailableNotifications()
	except exceptions.SPS_UserError as error:
		return error.message
	
	return json.dumps(result)

@app.route('/v0.1/login')
def api_login():
	try:
		result = functions.login()
	except exceptions.SPS_UserError as error:
		return error.message
	
	return json.dumps(result)

@app.route('/v0.1/acknowledgeNotification/<int:notificationId>')
def api_acknowledgeNotification(notificationId):
	try:
		result = functions.acknowledgeNotification(notificationId) 
	except exceptions.SPS_UserError as error:
		return error.message

	return json.dumps(result)

if __name__ == '__main__':
	app.run()
