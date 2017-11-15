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
   or 'No path parameters' if there are no path parameters
"""
def getMachines(event, context):
    buildingId = None
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
        filterExpression=Attr('buildingId').eq(buildingId)
        acceptedFilters = ['machineType', 'status']
        
        if event.get('queryStringParameters'):
	        for key in event.get('queryStringParameters'):
	            if key in acceptedFilters:
	                filterExpression = filterExpression & Attr(key).eq(event.get('queryStringParameters').get(key))
	    
        response = machineTable.scan(FilterExpression=filterExpression)
        if response.get('Items'):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response['Items'], cls=DecimalEncoder)
            }
        else:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Building or machines not found'})
            }
    else:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'No path parameters'})

        }
