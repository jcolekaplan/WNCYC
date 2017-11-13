import boto3
from decEncoder import *

"""Scan dynamo table"""
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
machineTable = dynamodb.Table('Machines')
response = machineTable.scan()

"""Lambda handler function for /buildings/{buildingId}/machines API call
   Returns all the machines in a given building if no queries specified
   If query (machineType and/or status) specified, filter machines matching those query parameters
   If no buildingId or queries are specified, return all machines
"""
def getMachines(event, context):

    buildingId = None
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
	
    machineType = None
    status = None
    if event.get('queryStringParameters'):
	    machineType = event.get('queryStringParameters').get('machineType')
	    status = event.get('queryStringParameters').get('status')

    if buildingId:
        machines = list()
        for machine in response['Items']:
            if buildingId == machine['buildingId']:
                if not machineType and not status:
                    machines.append(machine)
                elif machineType and machine['machineType']==machineType and not status:
                    machines.append(machine)
                elif status and machine['status']==status and not machineType:
                    machines.append(machine)
                elif machineType and status and machine['machineType']==machineType and machine['status']==status:
                    machines.append(machine)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(machines, cls=DecimalEncoder)
        }
 

    else:
        return {
            'statusCode': 200, 
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response["Items"], cls=DecimalEncoder)
        }
