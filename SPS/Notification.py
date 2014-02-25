from SPS.exceptions import *
import datetime
import sqlite3

class Notification():
	def __init__(self, requester, receiver, message, status='ARRIVED', created=None, expires=None, notificationId=None):
		self._status = status
		self.message = message
		self.requester = requester
		self.receiver = receiver

		if notificationId:
			# Re-creating object from database data
			self.notificationId = notificationId
			self.created = created
			self.expires = expires
		else:
			# New notification being created, persisting

			# Now, stored in UNIX timestamp format
			self.created = int(datetime.datetime.utcnow().strftime("%s"))

			# Default expiration in 15 minutes, stored in UNIX timstamp format
			self.expires = int((datetime.datetime.utcnow() + datetime.timedelta(minutes=15)).strftime("%s"))

			self.notificationId = None
			self.notificationId = self.persistNotification()

	def getMessage(self):
		return self.message

	def acknowledge(self):
		self.status = 'ACKNOWLEDGED'

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, status):
		try:
			assert status in ['ARRIVED', 'DELIVERED', 'ACKNOWLEDGED', 'FAILED']
		except AssertionError as error:
			raise SPS_UserError(2, "Invalid status '{0}' requested for notification {1}".format(status, self.notificationId))

		self._status = status

		# Updating in the peristent storage
		self.persistNotification()
	
	def persistNotification(self):
		# NOTE: with the incrase of the system's load, connecting each time to the dbfile and closing it might not scale.
		# A Singleton approach would be more scalable.

		with sqlite3.connect('sqlite3storage.db') as db:
			dbHandler = db.cursor()

			if self.notificationId:
				dbHandler.execute('UPDATE notifications SET status = ? WHERE id = ?', (self.status, self.notificationId))
				return self.notificationId
			else:
				dbHandler.execute('INSERT INTO notifications (status, message, requester, receiver, created, expires) VALUES (?, ?, ?, ?, ?, ?)', (self.status, self.message, self.requester, self.receiver, self.created, self.expires))
				return dbHandler.lastrowid
	
	def to_dict(self):
		return {
			'id': self.notificationId,
			'status': self._status,
			'message': self.message,
			'requester': self.requester,
			'receiver': self.receiver,
			'created': self.created,
			'expires': self.expires
		}

	#TODO: def readFromStorage():
