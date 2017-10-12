class Machine(object):
	"""Class representing all the data for a machine
	
	'attribute name': 'attribute type'
	swagger_types = {
		'status': 'str',
		'id': 'str',
		'buildingID': 'str',
		'machineType': 'str',
		'timeLeft': 'int',
		'isAvailable': 'bool'
	}
	
	'attribute name': 'attribute name in Swagger Doc'
	attribute_map = {
		'status': 'status',
		'id': 'id',
		'buildingID': 'buildingID',
		'machineType': 'machineType',
		'timeLeft': 'timeLeft',
		'isAvailable': 'isAvailable'
	}
	"""
	def __init__(self, status, ID, buildingID, machineType, timeLeft, isAvailable):
		"""Class instantiation
		
		Check if all the attributes are valid and assigns them if they are
		Raises ValueError if attributes are invalid
		"""
		allowed_status = ["success", "failure"]
		if status not in allowed_status:
			raise ValueError(
					"Invalid value for 'status' ({0}), must be one of {1}"
					.format(status, allowed_status))
		
		if ID is None:
			raise ValueError("Invalid value for 'ID', must not be 'None'")
			
		if buildingID is None:
			raise ValueError("Invalid value for 'buildingID', must not be 'None'")
			
		allowed_machineType = ["washer", "dryer"]
		if machineType not in allowed_machineType:
			raise ValueError(
					"Invalid value for 'machineType' ({0}), must be one of {1}"
					.format(machineType, allowed_machineType))
		
		if timeLeft is None:
			raiseValueError("Invalid value for 'timeLeft', must not be 'None'")
		
		self.status = status
		self.ID = ID
		self.buildingID = buildingID
		self.machineType = machineType
		self.timeLeft = timeLeft
		self.isAvailable = (timeLeft == 0)
		
	def status(self):
		"""Returns machine request status ("success" or "failure")"""
		return self.status
	
	def ID(self):
		"""Returns machine ID (i.e. "Barton Hall-2 Floor Dryer-12")"""
		return self.ID
	
	def buildingID(self):
		"""Returns ID of bulding machine is in (i.e. "Barton Hall-2 Floor")"""
		return self.buildingID
	
	def machineType(self):
		"""Returns machine type ("washer" or "dryer")"""
		return self.machineType
	
	def timeLeft(self):
		"""Returns time left in machine cycle"""
		return self.timeLeft
	
	def isAvailable(self):
		"""Returns machine availability (true or false)"""
		return self.isAvailable
	
