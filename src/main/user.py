class User(object):
	def __init__(self, userId, buildingName, buildingId):
        
		if userId is None:
			raise ValueError("Invalid value for 'userId', must not be 'None'")

		if buildingName is None:
			raise ValueError("Invalid value for 'buildingName', must not be 'None'")

		if buildingId is None:
			raise ValueError("Invalid value for 'buildingId', must not be 'None'")

		self.userId = userId
		self.buildingName = buildingName
		self.buildingId = buildingId
