class Machines(object):

	swagger_types = {
		'status': 'str',
		'id': 'str',
		'buildingID': 'str',
		'machineType': 'str',
		'timeLeft': 'int',
		'isAvailable': 'bool'
	}
	
	attribute_map = {
		'status': 'status',
		'id': 'id',
		'buildingID': 'buildingID',
		'machineType': 'machineType',
		'timeLeft': 'timeLeft',
		'isAvailable': 'isAvailable'
	}
	
	def __init__(self, status=None, id=None, buildingID=None, machineType=None, timeLeft=None, isAvailable=None):
	
		self._status = None
		self._id = None
		self._buildingID = None
		self._machineType = None
		self._timeLeft = None
		self._isAvailable = None
		
		if status is not None:
			self.status = status
		if id is not None:
			self.id = id
		if buildingID is not None:
			self.buildingID = buildingID
		if machineType is not None:
			self.machineType = machineType
		if timeLeft is not None:
			self.timeLeft = timeLeft
		if isAvailable is not None:
			self.isAvailable = isAvailable
	
	def status(self):
	
		return self._status
	
	def status(self, status):
	
		allowed = ["success", "failure"]
		if status not in allowed:
			raise ValueError(
				"Invalid value for 'status' ({0}), must be one of {1}"
				.format(status, allowed)
			)
		self._status = status
	
	def id(self):
	
		return self._id
	
	def id(self, id):
		
		self._id = id
		
	def buildingID(self):
		
		return self._buildingID
	
	def buildingID(self, buildingID):
	
		self._buildingID = buildingID
	
	def machineType(self):
	
		return self._machineType
	
	def machineType(self, machineType):
		
		allowed = ["washer", "dryer"]
		if machineType not in allowed:
			raise ValueError(
				"Invalid value for 'machineType' ({0}), must be one of {1}"
				.format(machineType, allowed)
			)
		self._machineType = machineType
	
	def timeLeft(self):
		
		return self._timeLeft
	
	def timeLeft(self, timeLeft):
		
		self._timeLeft = timeLeft
	
	def isAvailable(self):
		
		return self._isAvailable
	
	def isAvailable(self, timeLeft):
		
		self._isAvailable = (timeLeft == 0)