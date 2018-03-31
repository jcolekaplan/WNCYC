class Machine(object):
    
    def __init__(self, status, machineId, buildingId, machineType, timeLeft):
        """Class instantiation
        
        Check if all the attributes are valid and assigns them if they are
        Raises ValueError if attributes are invalid
        """
        if status is None:
            raise ValueError("Invalid value for 'status', must not be 'None'")
        
        if machineId is None:
            raise ValueError("Invalid value for 'machineId', must not be 'None'")
            
        if buildingId is None:
            raise ValueError("Invalid value for 'buildingId', must not be 'None'")
            
        allowedMachineTypes = ["washer", "dryer"]
        if machineType not in allowedMachineTypes:
            raise ValueError(
                    "Invalid value for 'machineType' ({0}), must be one of {1}"
                    .format(machineType, allowedMachineTypes))
        
        if timeLeft is None:
            raise ValueError("Invalid value for 'timeLeft', must not be 'None'")
        
        if timeLeft < -1:
            raise ValueError("Invalid value for 'timeLeft', must not be less than -1")
        
        if status.find('cycle') != -1:
            self.status = 'available'
        else:
            self.status = status
            
        self.machineId = machineId
        self.buildingId = buildingId
        self.machineType = machineType
        self.timeLeft = timeLeft
