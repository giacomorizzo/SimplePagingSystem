from flask import Flask, request, url_for, json
import logging
from SPS import exceptions
from SPS import functions

app = Flask(__name__)
app.debug = True

#TODO support multiple formats?

@app.route('/v0.1/createNotification', methods=['POST'])
@functions.requires_auth
def api_createNotification():
	try:
		result = functions.createNotification(request.form.get('message', None), request.form.get('receiver', None))
	except exceptions.SPS_UserError as error:
		return error.message

	return json.dumps(result)

@app.route('/v0.1/getNotification/<int:notificationId>')
@functions.requires_auth
def api_getNotification(notificationId):
	try:
		result = functions.getNotification(notificationId) 
	except exceptions.SPS_UserError as error:
		return error.message

	return json.dumps(result)

@app.route('/v0.1/getAvailableNotifications')
@functions.requires_auth
def api_getAvailableNotifications():
	try:
		result = functions.getAvailableNotifications()
	except exceptions.SPS_UserError as error:
		return error.message
	
	return json.dumps(result)

@app.route('/v0.1/acknowledgeNotification/<int:notificationId>')
@functions.requires_auth
def api_acknowledgeNotification(notificationId):
	try:
		result = functions.acknowledgeNotification(notificationId) 
	except exceptions.SPS_UserError as error:
		return error.message

	return json.dumps(result)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
