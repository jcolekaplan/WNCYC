import boto3
from decEncoder import *
from DynamoTable import *

def handler(event, context):
    """Scan dynamo table"""
    machineTable = DynamoTable('Machines')
    return getMachines(event, machineTable)

"""Lambda handler function for /buildings/{buildingId}/machines API call
   Returns all the machines in a given building
   or machines matching query parameters (machineType and/or status)
   or 'Building or machine not found' error if no machines are returned matching criteria
   or 'No path parameters' if there are no path parameters
"""
def getMachines(event, machineTable):
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
        filterExpression=Attr('buildingId').eq(buildingId)
        acceptedFilters = ['machineType', 'status']
        
        if event.get('queryStringParameters'):
	        for key in event.get('queryStringParameters'):
	            if key in acceptedFilters:
	                filterExpression = filterExpression & Attr(key).eq(event.get('queryStringParameters').get(key))
	    
        response = machineTable.scanFilter(filterExpression)
        if response.get('Items'):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response.get('Items'), cls=DecimalEncoder)
            }
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Building or machines not found'})
            }
    else:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'No path parameters'})
        }