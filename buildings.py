class Buildings(object):
	
	swagger_types = {
		'status': 'str',
		'id': 'str',
		'nameList': 'list[str]',
		'numWashers': 'int',
		'numDryers': 'int',
	}
	
	attribute_map = {
		'status': 'status',
		'id': 'id',
		'nameList': 'nameList',
		'numWashers': 'numWashers',
		'numDryers': 'numDryers'
	}
	
	def __init__(self, status=None, id=None, nameList=None, numWashers=None, numDryers=None):
		
		self._status = None
		self._id = None
		self._nameList = None
		self._numWashers = None
		self._numDryers = None
		
		if status is not None:
			self.status = status
		if id is not None:
			self.id = id
		if nameList is not None:
			self.nameList = nameList
		if numWashers is not None:
			self.numWashers = numWashers
		if numDryers is not None:
			self.numDryers = numDryers
		
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
	
	def nameList(self):
		
		return self._nameList
	
	def nameList(self, nameList):
	
		if nameList is None:
			raise ValueError("Invalid value for 'nameList', must not be 'None'")
		
		self._nameList = nameList
		
	def numWashers(self):
		
		return self._numWashers
	
	def numWashers(self, numWashers):
		
		self._numWashers = numWashers
	
	def numDryers(self):
		
		return self._numDryers
	
	def numDryers(self, numDryers):
		
		self_.numDryers = numDryers
		
		