import pytest

from ..main.machine import *

class TestMachine:
    
    # Available washer tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def avail_washer(self):
        availWasher = Machine("available", "colvin-1-floor-washer-02", "colvin-1-floor", "washer", 0)
        return availWasher
    
    def test_status_AW(self, avail_washer):
        assert avail_washer.status == "available"
        
    def test_machineId_AW(self, avail_washer):
        assert avail_washer.machineId == "colvin-1-floor-washer-02"
        
    def test_buildingId_AW(self, avail_washer):
        assert avail_washer.buildingId == "colvin-1-floor"
        
    def test_machineType_AW(self, avail_washer):
        assert avail_washer.machineType == "washer"
        
    def test_timeLeft_AW(self, avail_washer):
        assert avail_washer.timeLeft == 0
 
    # Non-available washer tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def nonAvail_washer(self):
        nonAvailWasher = Machine("est. time remaining 54 min", "colvin-1-floor-washer-02", "colvin-1-floor", "washer", 54)
        return nonAvailWasher
    
    def test_status_NW(self, nonAvail_washer):
        assert nonAvail_washer.status == "est. time remaining 54 min"
        
    def test_machineId_NW(self, nonAvail_washer):
        assert nonAvail_washer.machineId == "colvin-1-floor-washer-02"
        
    def test_buildingId_NW(self, nonAvail_washer):
        assert nonAvail_washer.buildingId == "colvin-1-floor"
        
    def test_machineType_NW(self, nonAvail_washer):
        assert nonAvail_washer.machineType == "washer"
        
    def test_timeLeft_NW(self, nonAvail_washer):
        assert nonAvail_washer.timeLeft == 54
    
    # Available dryer tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def avail_dryer(self):
        availDryer = Machine("available", "colvin-1-floor-dryer-05", "colvin-1-floor", "dryer", 0)
        return availDryer
    
    def test_status_AD(self, avail_dryer):
        assert avail_dryer.status == "available"
        
    def test_machineId_AD(self, avail_dryer):
        assert avail_dryer.machineId == "colvin-1-floor-dryer-05"
        
    def test_buildingId_AD(self, avail_dryer):
        assert avail_dryer.buildingId == "colvin-1-floor"
        
    def test_machineType_AD(self, avail_dryer):
        assert avail_dryer.machineType == "dryer"
        
    def test_timeLeft_AD(self, avail_dryer):
        assert avail_dryer.timeLeft == 0
        
    # Non-available dryer tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def nonAvail_dryer(self):
        nonAvailDryer = Machine("est. time remaining 13 min", "colvin-1-floor-dryer-05", "colvin-1-floor", "dryer", 13)
        return nonAvailDryer
    
    def test_status_ND(self, nonAvail_dryer):
        assert nonAvail_dryer.status == "est. time remaining 13 min"
        
    def test_machineId_ND(self, nonAvail_dryer):
        assert nonAvail_dryer.machineId == "colvin-1-floor-dryer-05"
        
    def test_buildingId_ND(self, nonAvail_dryer):
        assert nonAvail_dryer.buildingId == "colvin-1-floor"
        
    def test_machineType_ND(self, nonAvail_dryer):
        assert nonAvail_dryer.machineType == "dryer"
        
    def test_timeLeft_ND(self, nonAvail_dryer):
        assert nonAvail_dryer.timeLeft == 13
        
    # Cycle ended tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def cycle_ended(self):
        cycleEnded = Machine("cycle ended 6 minutes ago", "colvin-1-floor-washer-01", "colvin-1-floor", "washer", 0)
        return cycleEnded

    def test_status_CE(self, cycle_ended):
        assert cycle_ended.status == "available"
        
    def test_machineId_CE(self, cycle_ended):
        assert cycle_ended.machineId == "colvin-1-floor-washer-01"
        
    def test_buildingId_CE(self, cycle_ended):
        assert cycle_ended.buildingId == "colvin-1-floor"
        
    def test_machineType_CE(self, cycle_ended):
        assert cycle_ended.machineType == "washer"
        
    def test_timeLeft_CE(self, cycle_ended):
        assert cycle_ended.timeLeft == 0
        
    # Door still closed tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def door_closed(self):
        doorClosed = Machine("cycle has ended - door still closed", "colvin-1-floor-washer-01", "colvin-1-floor", "washer", -1)
        return doorClosed
        
    def test_status_DC(self, door_closed):
        assert door_closed.status == "available"
        
    def test_machineId_DC(self, door_closed):
        assert door_closed.machineId == "colvin-1-floor-washer-01"
        
    def test_buildingId_DC(self, door_closed):
        assert door_closed.buildingId == "colvin-1-floor"
        
    def test_machineType_DC(self, door_closed):
        assert door_closed.machineType == "washer"
        
    def test_timeLeft_DC(self, door_closed):
        assert door_closed.timeLeft == -1

    # Out of service tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def out_of_service(self):
        outOfService = Machine("out of service", "colvin-1-floor-washer-05", "colvin-1-floor", "washer", -1)
        return outOfService
        
    def test_status_OS(self, out_of_service):
        assert out_of_service.status == "out of service"
        
    def test_machineId_OS(self, out_of_service):
        assert out_of_service.machineId == "colvin-1-floor-washer-05"
        
    def test_buildingId_OS(self, out_of_service):
        assert out_of_service.buildingId == "colvin-1-floor"
        
    def test_machineType_OS(self, out_of_service):
        assert out_of_service.machineType == "washer"
        
    def test_timeLeft_OS(self, out_of_service):
        assert out_of_service.timeLeft == -1       

    # Unknown machine tests ==================================================
    @pytest.yield_fixture(autouse=True)
    def unknown(self):
        Unknown = Machine("unknown", "colvin-1-floor-washer-05", "colvin-1-floor", "washer", -1)
        return Unknown
        
    def test_status_UN(self, unknown):
        assert unknown.status == "unknown"
        
    def test_machineId_UN(self, unknown):
        assert unknown.machineId == "colvin-1-floor-washer-05"
        
    def test_buildingId_UN(self, unknown):
        assert unknown.buildingId == "colvin-1-floor"
        
    def test_machineType_UN(self, unknown):
        assert unknown.machineType == "washer"
        
    def test_timeLeft_UN(self, unknown):
        assert unknown.timeLeft == -1  
        
    # ValueError tests ==================================================
    def test_NoneMachine(self):
        with pytest.raises(ValueError):
            noneMachine = Machine(None, None, None, None, None)
            
    def test_NoneStatus(self):
        with pytest.raises(ValueError):
            noneStatus = Machine(None, "colvin-1-floor-washer-02", "colvin-1-floor", "washer", 0)
            
    def test_NoneMachineID(self):
        with pytest.raises(ValueError):
            nonMachineID = Machine("available", None, "colvin-1-floor", "washer", 0)
            
    def test_NoneBuildingID(self):
        with pytest.raises(ValueError):
            noneBuildingID = Machine("available", "colvin-1-floor-washer-02", None, "washer", 0)
            
    def test_NoneMachineType(self):
        with pytest.raises(ValueError):
            noneMachineType = Machine("available", "colvin-1-floor-washer-02", "colvin-1-floor", None, 0)
            
    def test_NoneTimeLeft(self):
        with pytest.raises(ValueError):
            NoneTimeLeft = Machine("available", "colvin-1-floor-washer-02", "colvin-1-floor", "washer", None)
            
    def test_InvalidMachineType(self):
        with pytest.raises(ValueError):
            InvalidMachineType = Machine("available", "colvin-1-floor-washer-02", "colvin-1-floor", "woosher", 0)
                     
    def test_NegTimeLeft(self):
        with pytest.raises(ValueError):
            NegTimeLeft = Machine("available", "colvin-1-floor-washer-02", "colvin-1-floor", "washer", -77)
