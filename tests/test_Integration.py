from nose.tools import *
import requests
import json

notification = None
auth = ('username', 'password')

def test_noAuth():
	r = requests.get('http://localhost:5000/v0.1/getAvailableNotifications')
	print(repr(r.text))

	assert r.status_code == 401

def test_getAvailableNotifications_empty():
	global auth

	r = requests.get('http://localhost:5000/v0.1/getAvailableNotifications', auth=auth)
	print(repr(r.text))

	assert r.status_code == 200
	assert r.json() ==  []

def test_getUnexistent_Notification():
	global auth

	r = requests.get('http://localhost:5000/v0.1/getNotification/1', auth=auth)
	print(repr(r.text))

	assert r.status_code == 200
	assert r.text == "The specified notification '1' doesn't exists or is not destinated to you"

def test_createNotification():
	global notification, auth

	r = requests.post('http://localhost:5000/v0.1/createNotification', data={'message': 'test message', 'receiver': 'username'}, auth=auth)
	print(repr(r.text))

	assert r.status_code == 200
	notification = r.json()
	assert notification['message'] == 'test message'
	assert notification['status'] == 'ARRIVED'

def test_getNotification():
	global notification, auth

	r = requests.get('http://localhost:5000/v0.1/getNotification/{0}'.format(notification['id']), auth=auth)
	print(repr(r.text))

	assert r.status_code == 200
	result = r.json()
	assert result['id'] == notification['id']
	assert notification['status'] == 'ARRIVED'

def test_getAvailableNotifications():
	global notification, auth

	r = requests.get('http://localhost:5000/v0.1/getAvailableNotifications', auth=auth)
	print(repr(r.text))

	assert r.status_code == 200
	notifications = r.json()
	assert len(notifications) == 1
	assert notifications[0]['id'] == notification['id']
	assert notifications[0]['status'] == 'DELIVERED'

def test_acknowledgeNotification():
	global notification, auth

	r = requests.get('http://localhost:5000/v0.1/acknowledgeNotification/{0}'.format(notification['id']), auth=auth)
	print(repr(r.text))

	assert r.status_code == 200
	result = r.json()
	assert result['id'] == notification['id']
	assert result['status'] == 'ACKNOWLEDGED'
