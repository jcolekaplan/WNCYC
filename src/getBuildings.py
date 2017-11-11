import json
import boto3
import decimal
from buildingsInfo import *

"""Scan dynamo table"""
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
buildingTable = dynamodb.Table('Buildings')
response = buildingTable.scan()

"""Workaround for formatting issue
   Source: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html
"""
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

"""Lambda handler function for /buildings API call
   Returns all the buildings if no friendlyName specified
   or just the one building containing the friendlyName
   or 'Building not found' error if friendlyName not in any list
"""
def getBuildings(event, context):
    """If friendlyName specified, assign it to variable,
       iterate through all the items in scanned dynamo table until finding it
       put it in JSON format and return
    """
    friendlyName = None
    if event.get('queryStringParameters'):
        friendlyName = event.get('queryStringParameters').get('friendlyName')
		
    if friendlyName:
        for building in response['Items']:
            if friendlyName in building['nameList']:
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(building, cls=DecimalEncoder)
                }
        """Error if not found"""
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': 'Building not found'
        }

    else:
        return {
            'statusCode': 200, 
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response["Items"], cls=DecimalEncoder)
        }
