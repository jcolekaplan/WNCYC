import boto3
from utils import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource and table"""
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Users')

def getBuildingFromSession(intent, session):

    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False
    
    """Get building from User table"""
    if session.get('user'):
        userId = session.get('user').get('userId')
        response = table.get_item(Key = {'userId': userId})
        building = response.get('Item').get('buildingName')
        
        """Tell user their building"""
        if response.get('Item'):
            speechOutput, repromptText = yourBuildingIs(building)
        """Building not found"""
        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()
        
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))