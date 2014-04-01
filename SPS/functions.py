from SPS.exceptions import *
from SPS.Notification import Notification
import sqlite3

def _sql_get(sql):
	with sqlite3.connect('sqlite3storage.db') as db:
		db.row_factory = sqlite3.Row
		dbHandler = db.cursor()

		# notificationId is an int, as it's been converted at API level
		dbHandler.execute(sql)
		return dbHandler.fetchall()

def getNotificationById(notificationId):
	# notificationId is an int, as it's been converted at API level
	notification = _sql_get('SELECT * FROM notifications WHERE id = {0}'.format(notificationId))

	if len(notification):
		return dbOutputToNotification(notification[0])
	else:
		raise SPS_UserError(1, "The specified notification '{0}' doesn't exists".format(notificationId))


def dbOutputToNotification(dbdict):
	return Notification(notificationId = dbdict['id'], status = dbdict['status'], message = dbdict['message'], requester = dbdict['requester'], receiver = dbdict['receiver'], created = dbdict['created'], expires = dbdict['expires'] )

def getAvailableNotifications():
	#TODO is the user allowed to perform this action?

	dict_notifications = []
	for notification in _sql_get('SELECT * FROM notifications WHERE status not in ("ACKNOWLEDGED", "FAILED")'):
		notification = dbOutputToNotification(notification)
		notification.status = "DELIVERED"
		dict_notifications.append(notification.to_dict())

	return dict_notifications

def createNotification(message, requester, receiver):
	#TODO is the user allowed to perform this action?
	"""
	Stores the notification in the database
	Returns the new notificationId
	"""

	#TODO Translate requester username to uid
	#TODO Translate receiver username to uid

	if not message:
		raise SPS_UserError(0, "No notification message specified")

	return Notification(requester=requester, receiver=receiver, message=message).to_dict()

def login():
	raise NotImplemented()

def getNotification(notificationId):
	return getNotificationById(notificationId).to_dict()

def acknowledgeNotification(notificationId):
	# If SPS_UserError is raised, we want to propagate it to the caller
	notification = getNotificationById(notificationId)
	notification.acknowledge()

	return notification.to_dict()
