from SPS.exceptions import *
from SPS.Notification import Notification
import sqlite3

def getNotificationById(notificationId):
	with sqlite3.connect('sqlite3storage.db') as db:
		db.row_factory = sqlite3.Row
		dbHandler = db.cursor()

		# notificationId is an int, as it's been converted at API level
		dbHandler.execute('SELECT * FROM notifications WHERE id = ?', (int(notificationId),))
		notification = dbHandler.fetchone()

	if notification:
		return dbOutputToNotification(notification)
	else:
		raise SPS_UserError(1, "The specified notification '{0}' doesn't exists".format(notificationId))


def dbOutputToNotification(dbdict):
	return Notification(notificationId = dbdict['id'], status = dbdict['status'], message = dbdict['message'], requester = dbdict['requester'], receiver = dbdict['receiver'], created = dbdict['created'], expires = dbdict['expires'] )

def getAvailableNotifications():
	#TODO is the user allowed to perform this action?

	with sqlite3.connect('sqlite3storage.db') as db:
		db.row_factory = sqlite3.Row
		dbHandler = db.cursor()

		dbHandler.execute('SELECT * FROM notifications WHERE status not in ("ACKNOWLEDGED", "FAILED")')
		notifications = dbHandler.fetchall()

		dict_notifications = []
		for notification in notifications:
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

	#TODO: return what?
	return notification.to_dict()
