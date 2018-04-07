import pytest
from unittest.mock import MagicMock
from ..main.dynamoTable import *
from ..main.building import *
from ..main.machine import *

class TestDynamoTable:
    # User table tests =========================================================
    @pytest.yield_fixture(autouse=True)
    def user_table(self):
        userTable = DynamoTable('Users')
        return userTable
    
    @pytest.yield_fixture(autouse=True)
    def mock_user(self):
        mockUser = MagicMock("Jacob")
        return mockUser  
    
    def test_UserTable(self, user_table):
        copy_UserTable = DynamoTable('Users')
        assert user_table.table == copy_UserTable.table
        
    def test_UserPut(self, user_table, mock_user):
        user_table.put = MagicMock(name = 'put')
        user_table.put(mock_user)
        user_table.put.assert_called_with(mock_user)
        
    def test_UserGet(self, user_table, mock_user):
        user_table.get = MagicMock(name = 'get')
        user_table.get(UserId = mock_user)
        user_table.get.assert_called_with(UserId = mock_user)
        
    def test_UserGetValError(self, user_table, mock_user):
        with pytest.raises(ValueError):
            user_table.get = MagicMock(side_effect=ValueError('No key found or too many given'))
            user_table.get(UserId = mock_user)
    
    # Building table tests =====================================================
    @pytest.yield_fixture(autouse=True)
    def building_table(self):
        buildingTable = DynamoTable('Buildings')
        return buildingTable
    
    @pytest.yield_fixture(autouse=True)
    def mock_building(self):
        mockBuilding = MagicMock("Colvin-1-floor")
        return mockBuilding  
    
    def test_BuildingTable(self, building_table):
        copy_BuildingTable = DynamoTable('Buildings')
        assert building_table.table == copy_BuildingTable.table
        
    def test_BuildingPut(self, building_table, mock_building):
        building_table.put = MagicMock(name = 'put')
        building_table.put(mock_building)
        building_table.put.assert_called_with(mock_building)
        
    def test_BuildingGet(self, building_table, mock_building):
        building_table.get = MagicMock(name = 'get')
        building_table.get(BuildingId = mock_building)
        building_table.get.assert_called_with(BuildingId = mock_building)
        
    def test_getBuildingValError(self, building_table, mock_building):
        with pytest.raises(ValueError):
            building_table.get = MagicMock(side_effect=ValueError('No key found or too many given'))
            building_table.get(BuildingId = mock_building)
            
    # Machine table tests ======================================================
    @pytest.yield_fixture(autouse=True)
    def machine_table(self):
        machineTable = DynamoTable('Machines')
        return machineTable
    
    @pytest.yield_fixture(autouse=True)
    def mock_machine(self):
        mockMachine = MagicMock('Colvin-1-floor-washer-02')
        return mockMachine  
    
    def test_MachineTable(self, machine_table):
        copy_MachineTable = DynamoTable('Machines')
        assert machine_table.table == copy_MachineTable.table
        
    def test_MachinePut(self, machine_table, mock_machine):
        machine_table.put = MagicMock(name = 'put')
        machine_table.put(mock_machine)
        machine_table.put.assert_called_with(mock_machine)
        
    def test_MachineGet(self, machine_table, mock_machine):
        machine_table.get = MagicMock(name = 'get')
        machine_table.get(MachineId = mock_machine)
        machine_table.get.assert_called_with(MachineId = mock_machine)
        
    def test_getMachineValError(self, machine_table, mock_machine):
        with pytest.raises(ValueError):
            machine_table.get = MagicMock(side_effect=ValueError('No key found or too many given'))
            machine_table.get(MachineId = mock_machine)

    # Scan table tests =========================================================
    def test_ScanUsers(self, user_table):
        user_table.scan = MagicMock(name = 'scan')
        user_table.scan()
        user_table.scan.assert_called_with()
        
    def test_ScanBuildings(self, building_table):
        building_table.scan = MagicMock(name = 'scan')
        building_table.scan()
        building_table.scan.assert_called_with()
        
    def test_ScanMachines(self, machine_table):
        machine_table.scan = MagicMock(name = 'scan')
        machine_table.scan()
        machine_table.scan.assert_called_with()
        
    # Scan filter tests ========================================================
    @pytest.yield_fixture(autouse=True)
    def mock_filter(self):
        mockFilter = MagicMock('filterExpression')
        return mockFilter
    
    def test_ScanfUsers(self, user_table, mock_filter):
        user_table.scanf = MagicMock(name = 'scanf')
        user_table.scanf(mock_filter)
        user_table.scanf.assert_called_with(mock_filter)
        
    def test_ScanfBuildings(self, building_table, mock_filter):
        building_table.scanf = MagicMock(name = 'scanf')
        building_table.scanf(mock_filter)
        building_table.scanf.assert_called_with(mock_filter)
        
    def test_ScanfMachines(self, machine_table, mock_filter):
        machine_table.scanf = MagicMock(name = 'scanf')
        machine_table.scanf(mock_filter)
        machine_table.scanf.assert_called_with(mock_filter)

    # Other ValueError tests ===================================================
    def test_InvalidType(self):
        with pytest.raises(ValueError):
            invalidType = MagicMock(side_effect=ValueError('No key found or too many given'))
            invalidTable = DynamoTable(invalidType)