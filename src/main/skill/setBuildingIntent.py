import boto3
from utils import *
from dynamoTable import *
from user import *

def setBuildingInSession(intent, session):
    """Dynamo resource and table"""
    userTable = DynamoTable('Users')
    return buildSetBuildingResponse(intent, session, userTable)
    
def createBuildingAttributes(building):
    return {'building': building}

def buildSetBuildingResponse(intent, session, userTable):
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

            userId = session.get('user').get('userId')
            buildingId = findBuilding.get('buildingId')
            newUser = User(userId, building, buildingId)
            userTable.put(newUser)
            
            speechOutput, repromptText = yourBuildingIs(building)

        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()
                       
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))