import boto3
from utils import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource and table"""
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Users')


def getAvailMachines(intent, session):

    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False
    
    """Get buildingId from User table and machineType from session
       Get available machines using API
       If there are available machines, tell user how many
       If not, offer to set a timer
    """
    if session.get('user'):
        userId = session.get('user').get('userId')
        response = table.get_item(Key = {'userId': userId})
        
        if response.get('Item'):
            buildingId = response.get('Item').get('buildingId')
            machineType = intent.get('slots').get('machineType').get('value')
            
            """Allow for user to use plurals when interacting with Alexa"""
            if machineType=='washers': 
                machineType = 'washer'
            elif machineType == 'dryers':
                machineType = 'dryer'
            
            """API Call /buildings/buildingId/machines?=available&machineType=machineType"""
            machineInfo = callApi(
                url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines?status=available&machineType={}'
                .format(buildingId, machineType)
            )
            if machineInfo != {'error': 'Building or machines not found'}:
                numAvailMachines = len(machineInfo)
                speechOutput = 'There are {} available {}s in your building right now'.format(str(numAvailMachines), machineType)
                repromptText = 'There are {} available {}s in your building right now'.format(str(numAvailMachines), machineType)
            else:
                speechOutput = 'There are no available {}s in your building right now.'\
                               'I can let you know when one is available if you say, '\
                               'let me know when a {} is available.'.format(machineType, machineType)
                repromptText = 'I can let you know when a {} is available if you say, '\
                               'let me know when a {} is available.'.format(machineType, machineType) 
                               
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