from SPS.exceptions import *
import datetime
import sqlite3
import logging

logging.basicConfig(filename='logs/SPS.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Notification():
	def __init__(self, requester, receiver, message, status='ARRIVED', created=None, expires=None, notificationId=None):
		self._status = status
		self.message = message
		self.requester = requester
		self.receiver = receiver

		if notificationId:
			logging.debug('NotificationId = {0}, not persisting'.format(notificationId))

			# Re-creating object from database data
			self.notificationId = notificationId
			self.created = created
			self.expires = expires

			expire_time = datetime.datetime.fromtimestamp(int(expires))
			if self.status == 'DELIVERED' and expire_time <= datetime.datetime.utcnow():
				# Acknowledgement didn't happen within 15 minutes
				logging.info('NotificationId: {0}, Status: {1}, Notification exired'.format(notificationId, self.status))
				self.status = 'FAILED'

			elif self.status == 'ARRIVED' and (expire_time - datetime.timedelta(minutes=10)) <= datetime.datetime.utcnow():
				# Delivery didn't happen within 5 minutes
				logging.info('NotificationId: {0}, Status: {1}, Notification delivery exired'.format(notificationId, self.status))
				self.status = 'FAILED'
		else:
			# New notification being created, persisting
			logging.debug('New notification. Persisting')

			# Now, stored in UNIX timestamp format
			self.created = int(datetime.datetime.utcnow().strftime("%s"))

			# Default expiration in 15 minutes, stored in UNIX timstamp format
			self.expires = int((datetime.datetime.utcnow() + datetime.timedelta(minutes=15)).strftime("%s"))

			self.notificationId = None
			self.notificationId = self.persistNotification()

	def getMessage(self):
		return self.message

	def acknowledge(self):
		logging.debug('Acknowledging notification {0}'.format(self.notificationId))
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

		logging.debug('NotificationId: {0}, Status set to {1}'.format(self.notificationId, status))
		self._status = status

		# Updating in the peristent storage
		self.persistNotification()
	
	def persistNotification(self):
		if self.notificationId:
			return self._sql_update('UPDATE notifications SET status = "{0}" WHERE id = "{1}"'.format(self.status, self.notificationId))
		else:
			return self._sql_update('INSERT INTO notifications (status, message, requester, receiver, created, expires) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format(self.status, self.message, self.requester, self.receiver, self.created, self.expires))
	
	def _sql_update(self, sql):
		# NOTE: with the incrase of the system's load, connecting each time to the dbfile and closing it might not scale.
		# A Singleton approach would be more scalable.

		logging.info('New SQL request')
		logging.debug('SQL: {0}'.format(sql))

		try:
			with sqlite3.connect('sqlite3storage.db') as db:
				dbHandler = db.cursor()
				dbHandler.execute(sql)

				return dbHandler.lastrowid

		except sqlite3.Error as e:
			raise SPS_Fatal(0, "Issues encountered while connecting to the database: '{0}'".format(e.args[0]))

	def to_dict(self):
		result = self.__dict__
		result['status'] = result.pop('_status')
		result['id'] = result.pop('notificationId')
		return result
