from nose.tools import *
import requests
import json

notification = None

def test_getAvailableNotifications_empty():
#	r = requests.get('https://api.github.com/user', auth=('user', 'pass'))

	# Test nr.1: at start, there should be no available notifications returned
	r = requests.get('http://localhost:5000/v0.1/getAvailableNotifications')
	assert r.status_code == 200
	assert r.json() ==  []

def test_getUnexistent_Notification():
	# Test nr.2: if we try to get an unexistent notification, we get an error back
	r = requests.get('http://localhost:5000/v0.1/getNotification/1')
	assert r.status_code == 200
	assert r.text == "The specified notification '1' doesn't exists"

def test_createNotification():
	global notification

	# Test nr.3: attempt to put a notification
	r = requests.post('http://localhost:5000/v0.1/createNotification', data={'message': 'test message'})
	assert r.status_code == 200

	notification = r.json()
	assert notification['message'] == 'test message'
	assert notification['status'] == 'ARRIVED'

def test_getNotification():
	global notification

	r = requests.get('http://localhost:5000/v0.1/getNotification/{0}'.format(notification['id']))
	assert r.status_code == 200
	result = r.json()
	assert result['id'] == notification['id']
	assert notification['status'] == 'ARRIVED'

def test_getAvailableNotifications():
	global notification

	r = requests.get('http://localhost:5000/v0.1/getAvailableNotifications')
	assert r.status_code == 200
	notifications = r.json()
	assert len(notifications) == 1
	assert notifications[0]['id'] == notification['id']
	assert notifications[0]['status'] == 'DELIVERED'

def test_acknowledgeNotification():
	global notification

	r = requests.get('http://localhost:5000/v0.1/acknowledgeNotification/{0}'.format(notification['id']))
	assert r.status_code == 200
	result = r.json()
	assert result['id'] == notification['id']
	assert result['status'] == 'ACKNOWLEDGED'
