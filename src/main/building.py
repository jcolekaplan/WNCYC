class Building(object):
	"""Class representing all the data for a building
	
	'attribute name': 'type'
	swagger_types = {
		'buildingId': 'str',
		'nameList': 'list[str]',
		'numWashers': 'int',
		'numDryers': 'int',
	}
	
	'attribute name': 'Attribute name in Swagger Docs'
	attribute_map = {
		'buildingId': 'buildingId',
		'nameList': 'nameList',
		'numWashers': 'numWashers',
		'numDryers': 'numDryers'
	}
	"""
	
	def __init__(self, buildingId, nameList, numWashers, numDryers):
		"""Class instatiation
		
		Check if all the attributes are valid and assigns them if they are
		Raises ValueError if attributes are invalid
		"""		
		if buildingId is None:
			raise ValueError("Invalid value for 'buildingId', must not be 'None'")
		
		if nameList is None:
			raise ValueError("Invalid value for 'nameList', must not be 'None'")
		
		if numWashers is None:
			raise ValueError("Invalid value for 'numWashers', must not be 'None'")
		
		if type(numWashers) is not int:
			raise ValueError("Invalid value for 'numWashers', must be an integer")		
		
		if numWashers < 0:
			raise ValueError("Invalid value for 'numWashers', must not be negative")				
			
		if numDryers is None:
			raise ValueError("Invalid value for 'numDryers', must not be'None'")
		
		if type(numDryers) is not int:
			raise ValueError("Invalid value for 'numDryers', must be an integer")
		
		if numDryers < 0:
			raise ValueError("Invalid value for 'numDryers', must not be negative")
		
		self.buildingId = buildingId
		self.nameList = nameList
		self.numWashers = numWashers
		self.numDryers = numDryers