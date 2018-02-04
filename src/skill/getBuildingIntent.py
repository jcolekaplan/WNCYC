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
        
        if response.get('Item'):
            speechOutput = 'Your building is {}. '\
                           'You can hear your building name again by saying, '\
                           'what is my building?'.format(response.get('Item').get('buildingName'))
            repromptText = 'You can hear your building name again by saying, what is my building?'
            
        else:
            """No valid building for user in User table"""
            speechOutput = 'I could not find your building.'\
                           'You can tell me your building by saying, my building is.'
            repromptText = 'You can tell me your building by saying, my building is.'
    
    else:
        """No user with that ID found in User table"""
        speechOutput = 'I am sorry. I do not know what your building is.'\
                       'You can tell me your building by saying, my building is.'
        repromptText = 'You can tell me your building by saying, my building is.'

    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))