import boto3
from decEncoder import *
from DynamoTable import *

def handler(event, context):
    """Dynamo resource"""
    buildingTable = DynamoTable('Buildings')
    return getBuildingId(event, buildingTable)

"""Lambda handler function for /buildings/{buildingId} API call
   Returns building with the buildingId specified in the path
   or 'Building not found' error if buildingId not found by query search
"""
def getBuildingId(event, buildingTable):
    """If buildingId specified, assign it to variable,
       use get_item to find it in building table
       put it in JSON format and return
    """
    if event.get('pathParameters'):
        buildingIdVal = event.get('pathParameters').get('buildingId')
        response = buildingTable.get(buildingId=buildingIdVal)
        if response.get('Item'):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response.get('Item'), cls=DecimalEncoder)
            }
        else:
            """Error if not found"""
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Building not found'})
            }
    else:
        """No path parameters"""	
        return {
	    'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
	    'body': json.dumps({'error': 'Path not found'})
	}
