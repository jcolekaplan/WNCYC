import boto3
from decEncoder import *
from fuzzywuzzy import fuzz
from dynamoTable import *

"""Scan dynamo table"""
#dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
#buildingTable = dynamodb.Table('Buildings')
buildingTable = dynamoTable('Buildings')

"""Lambda handler function for /buildings API call
   Returns all the buildings if no friendlyName specified
   or just the one building containing the friendlyName
   or 'Building not found' error if friendlyName not in any list
"""
def getBuildings(event, context):
    """Scan table"""
    #response = buildingTable.scan()
    response = buildingTable.scanTable()
    """If friendlyName specified, assign it to variable,
       iterate through all the items in scanned dynamo table until finding it
       put it in JSON format and return
    """
    if event.get('queryStringParameters'):
        friendlyName = event.get('queryStringParameters').get('friendlyName')
        for building in response.get('Items'):
            for name in building.get('nameList'):
                if fuzz.ratio(friendlyName.lower(), name) > 90 or friendlyName in building.get('nameList'):
                    """Found friendlyName"""
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps(building, cls=DecimalEncoder)
                    }
        """friendlyName does not match any building"""
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'friendlyName does not match any buildings'})
        }
    else:
        """Return all buildings"""
        return {
            'statusCode': 200, 
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response.get('Items'), cls=DecimalEncoder)
        }