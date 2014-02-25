class SPS_Fatal(Exception):
	"""
	The application has encountered an unrecoverable error and gets terminated.
	"""
	def __init__(self, errorId, message):
		self.errorId = errorId
		self.message = message

	# TODO update_metrics()

class SPS_Error(Exception):
	"""
	The application has encountered an error. A retry is attempted.
	"""
	def __init__(self, errorId, message):
		self.errorId = errorId
		self.message = message

	# TODO update_metrics()

class SPS_UserError(Exception):
	"""
	The user has generated an invalid request. An error is returned
	"""
	def __init__(self, errorId, message):
		self.errorId = errorId
		self.message = message

	# TODO update_metrics()
