from SPS.exceptions import *
from SPS.Notification import Notification
from flask import request, Response
from functools import wraps
import sqlite3
import logging
import hashlib

logging.basicConfig(filename='logs/SPS.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def _sql_get(sql):
	logging.info('New SQL request')
	logging.debug('SQL: {0}'.format(sql))

	try:
		with sqlite3.connect('sqlite3storage.db') as db:
			db.row_factory = sqlite3.Row
			dbHandler = db.cursor()

			# notificationId is an int, as it's been converted at API level
			dbHandler.execute(sql)
			return dbHandler.fetchall()
	except sqlite3.Error as e:
		raise SPS_Fatal(0, "Issues encountered while connecting to the database: '{0}'".format(e.args[0]))

def getNotificationById(notificationId):
	# notificationId is an int, as it's been converted at API level
	logging.debug('Querying for notificationId: {0}'.format(notificationId))

	requester_uid = request.authorization.uid
	notification = _sql_get('SELECT * FROM notifications WHERE id = {0} AND (receiver = {1} OR requester = {1})'.format(notificationId, requester_uid))

	if len(notification):
		logging.debug('Query returned {0} results'.format(len(notification)))
		notification = dbOutputToNotification(notification[0])
		return notification
	else:
		raise SPS_UserError(1, "The specified notification '{0}' doesn't exists or is not destinated to you".format(notificationId))


def mapUidToUsername(uid):
	return _sql_get('SELECT username FROM users WHERE uid = "{0}"'.format(uid))[0]['username']

def dbOutputToNotification(dbdict):
	return Notification(notificationId = dbdict['id'], status = dbdict['status'], message = dbdict['message'], requester = dbdict['requester'], receiver = dbdict['receiver'], created = dbdict['created'], expires = dbdict['expires'] )

def getAvailableNotifications():
	requester_uid = request.authorization.uid

	dict_notifications = []
	notifications = _sql_get("SELECT * FROM notifications WHERE status not in ('ACKNOWLEDGED', 'FAILED') AND receiver = {0}".format(requester_uid))
	logging.debug('Query returned {0} results'.format(len(notifications)))

	for notification in notifications:
		notification = dbOutputToNotification(notification)
		notification.status = "DELIVERED"
		dict_notifications.append(presentNotification(notification))

	return dict_notifications

def createNotification(message, receiver):
	"""
	Stores the notification in the database
	Returns the new notificationId
	"""

	requester = request.authorization.username
	requester_uid = request.authorization.uid

	logging.info('New createNotification request')
	logging.debug('Message: {0}, Requester: {1}, Receiver: {2}'.format(message, requester, receiver))

	if not message:
		raise SPS_UserError(0, "No notification message specified")
	
	if not receiver:
		raise SPS_UserError(0, "No receiver specified")

	receiver_uid = _sql_get("SELECT uid FROM users WHERE username = '{0}'".format(receiver))[0]['uid']

	if not receiver_uid:
		raise SPS_UserError(0, "Invalid receiver")

	logging.debug('Notification created. Message: {0}, Requester: {1} (uid {2}), Receiver: {3} (uid {4})'.format(message, requester, requester_uid, receiver, receiver_uid))
	notification = Notification(requester=requester_uid, receiver=receiver_uid, message=message)
	return presentNotification(notification)

def getNotification(notificationId):
	notification = getNotificationById(notificationId)
	return presentNotification(notification)

def acknowledgeNotification(notificationId):
	logging.debug('Requesting acknowledgement of notificationId: {0}'.format(notificationId))

	# If SPS_UserError is raised, we want to propagate it to the caller
	notification = getNotificationById(notificationId)
	notification.acknowledge()

	return presentNotification(notification)

def check_auth(username, password):
	"""This function is called to check if a username password combination is valid."""

	uids = _sql_get("SELECT uid FROM users WHERE username = '{0}' AND password = '{1}' LIMIT 1".format(username, hashlib.md5(password.encode('utf-8')).hexdigest()))

	if len(uids):
		uid = uids[0]['uid']
		logging.debug("Successful login for user {0} (uid {1})".format(username, uid))
		request.authorization.uid = uid
		return True
	else:
		return False

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response('Could not verify your access level for that URL.\n' 'You have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def presentNotification(notification):
	notification.receiver = mapUidToUsername(notification.receiver)
	notification.requester = mapUidToUsername(notification.requester)
	return notification.to_dict()

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated
