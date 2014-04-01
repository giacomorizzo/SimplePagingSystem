import unittest.mock
from unittest.mock import MagicMock, patch, call
from nose.tools import *
from SPS import functions
from SPS import exceptions

values = {
	'requester': 'dummyRequester',
	'receiver': 'dummyReceiver',
	'message': 'notification content',
	'notificationId': 99999,
	'notificationDict': {},
	'mockNotification': {}
}

@patch('SPS.functions.dbOutputToNotification')
@patch('SPS.functions._sql_get')
def test_getNotificationById(mock_sqlGet, mock_dbOutputToNotification):
	return_list = [values['notificationDict']]
	mock_sqlGet.return_value = return_list
	mock_dbOutputToNotification.return_value = values['mockNotification']

	retval = functions.getNotificationById(values['notificationId'])

	assert retval == values['mockNotification']
	assert mock_dbOutputToNotification.call_count == 1
	assert mock_dbOutputToNotification.called_with(values['notificationDict'])

@raises(exceptions.SPS_UserError)
@patch('SPS.functions.dbOutputToNotification')
@patch('SPS.functions._sql_get')
def test_getNotificationById_notexistent(mock_sqlGet, mock_dbOutputToNotification):
	mock_sqlGet.return_value = []
	functions.getNotificationById(values['notificationId'])

	assert mock_sqlGet.call_count == 1
	assert mock_dbOutputToNotification.call_count == 0

def test_dbOutputToNotification():
	# Just a class instantiation wrapper
	pass

@patch('SPS.functions.dbOutputToNotification')
@patch('SPS.functions._sql_get')
def test_getAvailableNotifications(mock_sqlGet, mock_dbOutputToNotification):
	return_list = [values['notificationDict'], values['notificationDict']]
	mock_sqlGet.return_value = return_list
	mock_notification = MagicMock()
	mock_dbOutputToNotification.return_value = mock_notification

	retval = functions.getAvailableNotifications()

	assert len(retval) == len(return_list)
	assert mock_dbOutputToNotification.call_count == len(return_list)
	mock_dbOutputToNotification.assert_any_call(values['notificationDict'])
	assert mock_notification.mock_calls == [call.to_dict(), call.to_dict()]

@patch('SPS.functions.Notification')
def test_createNotification(mock_Notification):
	mock_toDict = MagicMock(return_value=values['notificationDict'])
	mock_Notification.return_value = MagicMock(to_dict=mock_toDict)

	retval = functions.createNotification(values['message'], values['requester'], values['receiver'])

	assert retval == values['notificationDict']
	assert mock_Notification.call_count == 1
	assert mock_toDict.call_count == 1

@raises(exceptions.SPS_UserError)
@patch('SPS.functions.Notification')
def test_createNotification_noMessage(mock_Notification):
	message = ''

	functions.createNotification(message, values['requester'], values['receiver'])

	assert mock_Notification.call_count == 0

def test_getNotification():
	# Just a wrapper for getNotificationById
	pass

@patch('SPS.functions.getNotificationById')
def test_acknowledgeNotification(mock_getNotificationById):
	mock_Notification = MagicMock()
	mock_getNotificationById.return_value = mock_Notification

	retval = functions.acknowledgeNotification(values['notificationId'])

	assert mock_getNotificationById.call_count == 1
	assert mock_Notification.mock_calls == [call.acknowledge(), call.to_dict()]
