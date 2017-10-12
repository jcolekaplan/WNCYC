class Building(object):
	"""Class representing all the data for a building
	
	'attribute name': 'type'
	swagger_types = {
		'status': 'str',
		'id': 'str',
		'nameList': 'list[str]',
		'numWashers': 'int',
		'numDryers': 'int',
	}
	
	'attribute name': 'Attribute name in Swagger Docs'
	attribute_map = {
		'status': 'status',
		'id': 'id',
		'nameList': 'nameList',
		'numWashers': 'numWashers',
		'numDryers': 'numDryers'
	}
	"""
	
	def __init__(self, status, ID, nameList, numWashers, numDryers):
		"""Class instatiation
		
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
		
		if nameList is None:
			raise ValueError("Invalid value for 'nameList', must not be 'None'")
		
		if numWashers is None:
			raise ValueError("Invalid value for 'numWashers', must not be 'None'")
		
		if numDryers is None:
			raise ValueError("Invalid value for 'numDryers', must not be'None'")
		
		self.status = status
		self.ID = ID
		self.nameList = nameList
		self.numWashers = numWashers
		self.numDryers = numDryers
		
	def status(self):
		"""Returns building request status ("success" or "failure")"""
		return self.status
		
	def ID(self):
		"""Returns building ID (i.e. "Barton Hall-2 Floor")"""
		return self.ID
		
	def nameList(self):
		"""Returns bulding friendly name list (i.e. ["Barton", "Barton Hall", "Hotel Barton", etc.])"""
		return self.nameList
		
	def numWashers(self):
		"""Returns the total number of washers in a building"""
		return self.numWashers
		
	def numDryers(self):
		"""Returns the total number of dryers in a building"""
		return self.numDryers
