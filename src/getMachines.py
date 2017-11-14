import boto3
from decEncoder import *
from boto3.dynamodb.conditions import Key, Attr

"""Scan dynamo table"""
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
machineTable = dynamodb.Table('Machines')

"""Lambda handler function for /buildings/{buildingId}/machines API call
   Returns all the machines in a given building
   or machines matching query parameters (machineType and/or status)
   or 'Building or machine not found' error if no machines are returned matching criteria
"""
def getMachines(event, context):
    buildingId = None
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
    if buildingId:
        machineType = None
        status = None
        if event.get('queryStringParameters'):
	        machineType = event.get('queryStringParameters').get('machineType')
	        status = event.get('queryStringParameters').get('status')
			
    	response = machineTable.scan(
	    	FilterExpression=Attr('buildingId').eq(buildingId)
		)
        elif machineType and not status:
            response = machineTable.scan(
                FilterExpression=(Attr('buildingId').eq(buildingId)
			    & Attr('machineType').eq(machineType))
            )
        elif status and not machineType:
            response = machineTable.scan(
                FilterExpression=(Attr('buildingId').eq(buildingId)
			    & Attr('status').eq(status))
            )
        elif status and machineType:
            response = machineTable.scan(
                FilterExpression=(Attr('buildingId').eq(buildingId)
                & Attr('machineType').eq(machineType)
    			& Attr('status').eq(status))
	    )
        if response.get('Items'):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response['Items'], cls=DecimalEncoder)
            }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Building or machines not found'})
    }
