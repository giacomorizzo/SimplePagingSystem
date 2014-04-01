import unittest.mock
from unittest.mock import MagicMock, patch
from nose.tools import *
from SPS import Notification
from SPS import exceptions
import datetime

values = {
	'message': 'message content',
	'receiver': 'receiver_username',
	'requester': 'requester_username',
	'last_row_id': 999,
	'notification_id': 10,
	'expires': (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%s'),
	'created': datetime.datetime.utcnow().strftime('%s'),
	'invalid_state': 'INVALID_STATE_1235'
}

@patch.object(Notification.Notification, 'persistNotification')
def test_Notification_new(mocked_method):
	# TODO
	pass

@patch.object(Notification.Notification, 'persistNotification')
def test_Notification_existent(mocked_method):
	# TODO
	pass

@patch.object(Notification.Notification, 'persistNotification')
def test_Notification_expired(mocked_method):
	# TODO
	pass

@patch.object(Notification.Notification, 'persistNotification')
def test_getMessage(mocked_method):
	# This will call persistNotification a first time
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'])

	assert instance.getMessage() is values['message']

@patch.object(Notification.Notification, 'persistNotification')
def test_acknowledge(mocked_method):
	# This will call persistNotification a first time
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'])

	instance.acknowledge()
	assert instance.status == 'ACKNOWLEDGED'
	assert instance.persistNotification.call_count == 2

@raises(exceptions.SPS_UserError)
@patch.object(Notification.Notification, 'persistNotification')
def test_status_setter_invalid(mocked_method):
	# This will call persistNotification a first time
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'])

	instance.status = values['invalid_state']
	assert instance.status == values['invalid_state']
	assert instance.persistNotification.call_count == 1

@patch.object(Notification.Notification, 'persistNotification')
def test_status_setter_valid(mocked_method):
	# This will call persistNotification a first time
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'])

	valid_statuses = ['ARRIVED', 'DELIVERED', 'ACKNOWLEDGED', 'FAILED']
	for status in valid_statuses:
		instance.status = status
		assert instance.status == status

	assert instance.persistNotification.call_count == len(valid_statuses)+1

@patch.object(Notification.Notification, '_sql_update')
def test_persistNotification_new(mocked_method):
	mocked_method.return_value = values['last_row_id']

	# Forcing a notificationId in the constructor to avoid calling persistNotification within the constructor
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'], expires=values['expires'], created=values['created'], status='DELIVERED', notificationId=1)
	assert mocked_method.call_count == 0

	# Now setting the notificationId to None to trigger the creation manually
	instance.notificationId = None
	
	return_id = instance.persistNotification()
	assert return_id == values['last_row_id']
	assert mocked_method.call_count == 1
	assert mocked_method.call_args[0][0].startswith('INSERT ')

@patch.object(Notification.Notification, '_sql_update')
def test_persistNotification_update(mocked_method):
	mocked_method.return_value = values['notification_id']

	# Forcing a notificationId in the constructor to avoid calling persistNotification within the constructor
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'], expires=values['expires'], created=values['created'], status='DELIVERED', notificationId=1)
	assert mocked_method.call_count == 0

	# Now setting the notificationId to None to trigger the creation manually
	instance.notificationId = values['notification_id']
	
	return_id = instance.persistNotification()
	assert return_id == values['notification_id']
	assert mocked_method.call_count == 1
	assert mocked_method.call_args[0][0].startswith('UPDATE ')

@patch.object(Notification.Notification, '_sql_update')
def test_persistNotification_expired(mocked_method):
	mocked_method.return_value = values['notification_id']

	# Testing the edge case: the notification expires in this very second
	expires = datetime.datetime.utcnow().strftime('%s')
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'], expires=expires, created=values['created'], status='DELIVERED', notificationId=1)

	assert instance.status == "FAILED"
	assert mocked_method.call_count == 1
	assert mocked_method.call_args[0][0].startswith('UPDATE ')

@patch.object(Notification.Notification, '_sql_update')
def test_persistNotification_expired_5m(mocked_method):
	mocked_method.return_value = values['notification_id']

	# Testing the edge case: the notification has just passed the 5 allowed minutes for delivery
	expires = datetime.datetime.utcnow().strftime('%s')
	instance = Notification.Notification(requester=values['requester'], receiver=values['receiver'], message=values['message'], expires=expires, created=values['created'], status='ARRIVED', notificationId=1)

	assert instance.status == "FAILED"
	assert mocked_method.call_count == 1
	assert mocked_method.call_args[0][0].startswith('UPDATE ')
