import boto3
from decEncoder import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource"""
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
buildingTable = dynamodb.Table('Buildings')

"""Lambda handler function for /buildings/{buildingId} API call
   Returns building with the buildingId specified in the path
   or 'Building not found' error if buildingId not found by query search
"""
def getBuildingId(event, context):
    """If buildingId specified, assign it to variable,
       use get_item to find it in building table
       put it in JSON format and return
    """
    buildingId = None
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
        response = buildingTable.get_item(Key={'buildingId': buildingId})
        if response.get('Item'):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response['Item'], cls=DecimalEncoder)
            }
        else:
            """Error if not found"""
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Building not found'})
            }
    """Error if path not specified"""
    return {
    'statusCode': 404,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps({'error': 'Path not found'})
    }
