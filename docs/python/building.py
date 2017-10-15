class Building(object):
	"""Class representing all the data for a building
	
	'attribute name': 'type'
	swagger_types = {
		'status': 'str',
		'buildingId': 'str',
		'nameList': 'list[str]',
		'numWashers': 'int',
		'numDryers': 'int',
	}
	
	'attribute name': 'Attribute name in Swagger Docs'
	attribute_map = {
		'status': 'status',
		'buildingId': 'buildingId',
		'nameList': 'nameList',
		'numWashers': 'numWashers',
		'numDryers': 'numDryers'
	}
	"""
	
	def __init__(self, status, buildingId, nameList, numWashers, numDryers):
		"""Class instatiation
		
		Check if all the attributes are valid and assigns them if they are
		Raises ValueError if attributes are invalid
		"""
		allowed_status = ["success", "failure"]
		if status not in allowed_status:
			raise ValueError(
					"Invalid value for 'status' ({0}), must be one of {1}"
					.format(status, allowed_status))
		
		if buildingId is None:
			raise ValueError("Invalid value for 'buildingId', must not be 'None'")
		
		if nameList is None:
			raise ValueError("Invalid value for 'nameList', must not be 'None'")
		
		if numWashers is None:
			raise ValueError("Invalid value for 'numWashers', must not be 'None'")
		
		if numDryers is None:
			raise ValueError("Invalid value for 'numDryers', must not be'None'")
		
		self.status = status
		self.buildingId = buildingId
		self.nameList = nameList
		self.numWashers = numWashers
		self.numDryers = numDryers
