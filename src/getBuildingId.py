import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource"""
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
buildingTable = dynamodb.Table('Buildings')

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

"""Lambda handler function for /buildings/{buildingId} API call
   Returns building with the buildingId specified in the path
   or 'Building not found' error if buildingId not found by query search
"""
def getBuildingId(event, context):
    """If buildingId specified, assign it to variable,
	   use query to find it in building table
       put it in JSON format and return
    """
    buildingId = None
    if event.get('pathParameters'):
        buildingId = event.get('pathParameters').get('buildingId')
		
        response = buildingTable.query(
                KeyConditionExpression=Key('buildingId').eq(buildingId)
        )
    	
        if len(response["Items"]):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response["Items"], cls=DecimalEncoder)
            }
        else:
            """Error if not found"""
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': 'Building not found'
            }
