import boto3
from decEncoder import *
from DynamoTable import *

def handler(event, context):
    """Dynamo resource"""
    machineTable = DynamoTable('Machines')
    return getMachineId(event, machineTable)

"""Lambda handler function for /buildings/{buildingId}/machines/{machineId} API call
   Returns machine with the machineId specified in the path
   or 'Building not found' if buildingId in machine found does not match buildingId in path
   or 'Machine not found' error if machineId not found by get_item search
   or 'No path parameters' if there are no path parameters
"""
def getMachineId(event, machineTable):
    """If machineId specified, assign it to variable,
       use get_item to find it in machine table
       put it in JSON format and return
    """
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
        machineIdVal = event.get('pathParameters').get('machineId')
        response = machineTable.get(machineId=machineIdVal)
        if response.get('Item'):
            if response.get('Item').get('buildingId')==buildingId:
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(response.get('Item'), cls=DecimalEncoder)
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
