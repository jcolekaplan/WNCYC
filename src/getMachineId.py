import boto3
from decEncoder import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource"""
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
machineTable = dynamodb.Table('Machines')

"""Lambda handler function for /buildings/{buildingId}/machines/{machineId} API call
   Returns machine with the machineId specified in the path
   or 'Building not found' if buildingId in machine found does not match buildingId in path
   or 'Machine not found' error if machineId not found by get_item search
   or 'No path parameters' if there are no path parameters
"""
def getMachineId(event, context):
    """If machineId specified, assign it to variable,
       use get_item to find it in machine table
       put it in JSON format and return
    """
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
        machineId = event.get('pathParameters').get('machineId')
        response = machineTable.get_item(Key={'machineId': machineId})
        if response.get('Item'):
            if response.get('Item').get('buildingId')==buildingId:
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(response['Item'], cls=DecimalEncoder)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Machine not found in that building'})
                }
        else:
            """Error if not found"""
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Machine not found'})
            }
    else:
        """No path parameters"""
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'No path parameters'})
        }
