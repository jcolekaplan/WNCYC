class Machine(object):
	"""Class representing all the data for a machine
	
	'attribute name': 'attribute type'
	swagger_types = {
		'status': 'str',
		'machineId': 'str',
		'buildingId': 'str',
		'machineType': 'str',
		'timeLeft': 'int',
		'isAvailable': 'bool'
	}
	
	'attribute name': 'attribute name in Swagger Doc'
	attribute_map = {
		'status': 'status',
		'machineId': 'machineId',
		'buildingId': 'buildingId',
		'machineType': 'machineType',
		'timeLeft': 'timeLeft',
		'isAvailable': 'isAvailable'
	}
	"""
	def __init__(self, status, machineId, buildingId, machineType, timeLeft, isAvailable):
		"""Class instantiation
		
		Check if all the attributes are valid and assigns them if they are
		Raises ValueError if attributes are invalid
		"""
		allowed_status = ["success", "failure"]
		if status not in allowed_status:
			raise ValueError(
					"Invalid value for 'status' ({0}), must be one of {1}"
					.format(status, allowed_status))
		
		if machineId is None:
			raise ValueError("Invalid value for 'machineId', must not be 'None'")
			
		if buildingId is None:
			raise ValueError("Invalid value for 'buildingId', must not be 'None'")
			
		allowed_machineType = ["washer", "dryer"]
		if machineType not in allowed_machineType:
			raise ValueError(
					"Invalid value for 'machineType' ({0}), must be one of {1}"
					.format(machineType, allowed_machineType))
		
		if timeLeft is None:
			raiseValueError("Invalid value for 'timeLeft', must not be 'None'")
		
		self.status = status
		self.machineId = machineId
		self.buildingId = buildingId
		self.machineType = machineType
		self.timeLeft = timeLeft
		self.isAvailable = (timeLeft == 0)
