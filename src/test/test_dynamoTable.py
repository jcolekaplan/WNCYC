import pytest
import boto3
from unittest.mock import patch, Mock
from ..main.dynamoTable import *
from ..main.building import *
from ..main.machine import *
from ..main.user import *

class TestDynamoTable:
    # User Table tests ============================================================================
    @patch('boto3.resource')
    def test_UserPut(self, mock_boto3):
        userTable = DynamoTable('Users')
        userTable.table.put_item = Mock(name='put_item')
        
        newUser = User('userId1', 'userBuilding', 'userBuildingID1')
        userTable.put(newUser)
        userTable.table.put_item.assert_called_once_with(Item=vars(newUser))

    @patch('boto3.resource')
    def test_UserGet(self, mock_boto3):
        userTable = DynamoTable('Users')
        test_output = {
            'User': {
                'userId': 'userId1',
                'buildingName': 'userBuilding',
                'buildingId': 'userBuildingID1'
            }
        }
        userTable.table.get_item = Mock(name='get_item', return_value=test_output)
        out = userTable.get(userId='userId1')
        assert out == test_output
        userTable.table.get_item.assert_called_once_with(Key={'userId': 'userId1'})
    
    @patch('boto3.resource')
    def test_UserScan(self, mock_boto3):
        userTable = DynamoTable('Users')
        test_output = {
            'scan': 'scanInfo'
        }
        userTable.table.scan = Mock(name='scan', return_value=test_output)
        out = userTable.scan()
        assert out == test_output
        userTable.table.scan.assert_called_once_with()
        
    @patch('boto3.resource')
    def test_UserScanf(self, mock_boto3):
        userTable = DynamoTable('Users')
        test_output = {
            'scanFilter': 'scanFilterInfo'
        }
        userTable.table.scan = Mock(name='scan', return_value=test_output)
        filterExpression = 'someFilter'
        out = userTable.scanf(filterExpression)
        assert out == test_output
        userTable.table.scan.assert_called_once_with(FilterExpression='someFilter')
        
    # Machine Table tests =========================================================================
    @patch('boto3.resource')
    def test_MachinePut(self, mock_boto3):
        machineTable = DynamoTable('Machines')
        machineTable.table.put_item = Mock(name='put_item')
        
        newMachine = Machine("available", "colvin-1-floor-washer-02", "colvin-1-floor", "washer", 0)
        machineTable.put(newMachine)
        machineTable.table.put_item.assert_called_once_with(Item=vars(newMachine))

    @patch('boto3.resource')
    def test_MachineGet(self, mock_boto3):
        machineTable = DynamoTable('Machines')
        test_output = {
            'Machine': {
                'status': 'available',
                'machineId': 'colvin-1-floor-washer-02',
                'buildingId': 'colvin-1-floor',
                'machineType': 'washer',
                'timeLeft': 0
            }
        }
        machineTable.table.get_item = Mock(name='get_item', return_value=test_output)
        out = machineTable.get(machineId='colvin-1-floor-washer-02')
        assert out == test_output
        machineTable.table.get_item.assert_called_once_with(Key={'machineId': 'colvin-1-floor-washer-02'})
    
    @patch('boto3.resource')
    def test_MachineScan(self, mock_boto3):
        machineTable = DynamoTable('Machines')
        test_output = {
            'scan': 'scanInfo'
        }
        machineTable.table.scan = Mock(name='scan', return_value=test_output)
        out = machineTable.scan()
        assert out == test_output
        machineTable.table.scan.assert_called_once_with()
        
    @patch('boto3.resource')
    def test_MachineScanf(self, mock_boto3):
        machineTable = DynamoTable('Machines')
        test_output = {
            'scanFilter': 'scanFilterInfo'
        }
        machineTable.table.scan = Mock(name='scan', return_value=test_output)
        filterExpression = 'someFilter'
        out = machineTable.scanf(filterExpression)
        assert out == test_output
        machineTable.table.scan.assert_called_once_with(FilterExpression='someFilter')

    # Building Table tests =========================================================================
    @patch('boto3.resource')
    def test_BuildingPut(self, mock_boto3):
        buildingTable = DynamoTable('Buildings')
        buildingTable.table.put_item = Mock(name='put_item')
        
        newBuilding = Building("colvin-1-floor", ["colvin", "colvin apartment"], 6, 6)
        buildingTable.put(newBuilding)
        buildingTable.table.put_item.assert_called_once_with(Item=vars(newBuilding))

    @patch('boto3.resource')
    def test_BuildingGet(self, mock_boto3):
        buildingTable = DynamoTable('Buildings')
        test_output = {
            'Building': {
                'buildingId': 'colvin-1-floor',
                'nameList': ["colvin", "colvin apartment"],
                'numWashers': 6,
                'numDryers': 6
            }
        }
        buildingTable.table.get_item = Mock(name='get_item', return_value=test_output)
        out = buildingTable.get(buildingId='colvin-1-floor')
        assert out == test_output
        buildingTable.table.get_item.assert_called_once_with(Key={'buildingId': 'colvin-1-floor'})
    
    @patch('boto3.resource')
    def test_BuildingScan(self, mock_boto3):
        buildingTable = DynamoTable('Buildings')
        test_output = {
            'scan': 'scanInfo'
        }
        buildingTable.table.scan = Mock(name='scan', return_value=test_output)
        out = buildingTable.scan()
        assert out == test_output
        buildingTable.table.scan.assert_called_once_with()
        
    @patch('boto3.resource')
    def test_BuildingScanf(self, mock_boto3):
        buildingTable = DynamoTable('Buildings')
        test_output = {
            'scanFilter': 'scanFilterInfo'
        }
        buildingTable.table.scan = Mock(name='scan', return_value=test_output)
        filterExpression = 'someFilter'
        out = buildingTable.scanf(filterExpression)
        assert out == test_output
        buildingTable.table.scan.assert_called_once_with(FilterExpression='someFilter')
    
    # ValueError tests ============================================================================
    @patch('boto3.resource')
    def test_InvalidTableType(self, mock_boto3):
        with pytest.raises(ValueError):
            invalidTable = DynamoTable('Invalid')
    
    @patch('boto3.resource')
    def test_InvalidKwargs(self, mock_boto3):
        buildingTable = DynamoTable('Buildings')
        with pytest.raises(ValueError):
            out = buildingTable.get(buildingId='colvin-1-floor', buildingId2='davison-hall-floor')
