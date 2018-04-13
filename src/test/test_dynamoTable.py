import pytest
import boto3
from unittest.mock import patch, MagicMock
from ..main.dynamoTable import *
from ..main.building import *
from ..main.machine import *

@patch("dynamodb.boto3")
def test_get(mock_boto3):
    dynamo = DynamoTable("Buildings")
    test_output = {
        "Item": {
            "test": "test"
        }
    }
    dynamo.table.get_item = Mock(name="get_item", return_value=test_output)
    out = dynamo.get(buildingId="1")
    assert out == test_output
    dynamo.table.get_item.assert_called_once_with(Key={"buildingId": "1"})
