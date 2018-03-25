import boto3
from utils import *

"""Dynamo resource and table"""
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Users')

def createBuildingAttributes(building):
    return {'building': building}

def setBuildingInSession(intent, session):
    """ Sets the building in the session and prepares the speech to reply to the user.
        Writes user ID to User table
    """
    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False

    if 'building' in intent.get('slots'):
        building = APIBuilding(intent)
        sessionAttributes = createBuildingAttributes(building)
        
        """Calls API /buildings?friendlyName=building to find valid buildingId"""
        findBuilding = APIFindBuilding(building)
        if findBuilding.get('buildingId'):
            userInfo = {
                'userId' : session.get('user').get('userId'),
                'buildingId' : findBuilding.get('buildingId'),
                'buildingName': building
            }
            table.put_item(Item=userInfo)
            speechOutput, repromptText = yourBuildingIs(building)

        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()
                       
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))