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
        building = intent.get('slots').get('building').get('value')
        sessionAttributes = createBuildingAttributes(building)
        speechOutput = 'I now know your building is ' + building.capitalize() + '. ' \
                       'You can ask me what your building is by saying, what is my building?'
        repromptText = 'You can ask me what your building is by saying, what is my building?'
        
        """Calls API /buildings?friendlyName=building to find valid buildingId"""
        findBuilding = callApi(
            "https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings?friendlyName={}".format(building).replace(' ', '%20')
        )
        if findBuilding.get('buildingId'):
            userInfo = {
                'userId' : session.get('user').get('userId'),
                'buildingId' : findBuilding.get('buildingId'),
                'buildingName': building
            }
            table.put_item(Item=userInfo)
        else:
            """Not a valid building"""
            speechOutput = 'I could not find that building. Please try again. '\
                           'You can tell me your building by saying, my building is.'
            repromptText = 'You can tell me your building by saying, my building is.'    

    else:
        """Building not found in session"""
        speechOutput = 'I am not sure what your building is. Please try again.'
        repromptText = 'I am not sure what your building is. Please try again.' \
                       'You can tell me your building by saying, my building is.'
                       
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))