import boto3
from utils import *
from dynamoTable import *
from boto3.dynamodb.conditions import Key, Attr

def getBuildingFromSession(intent, session):
    """Dynamo resource and table"""
    userTable = DynamoTable('Users')
    return buildBuildingFromSessionResponse(intent, session, userTable)

def buildBuildingFromSessionResponse(intent, session, userTable):

    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False
    
    """Get building from User table"""
    if session.get('user'):
        userIdVal = session.get('user').get('userId')
        response = userTable.get(userId=userIdVal)
        building = response.get('Item').get('buildingName')
        
        """Tell user their building"""
        if response.get('Item'):
            speechOutput, repromptText = yourBuildingIs(building)
        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()
        
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))