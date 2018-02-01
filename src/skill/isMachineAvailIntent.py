import boto3
from utils import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource and table"""
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Users')

def isMachineAvail(intent, session):

    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False
    
    """Get buildingId from User table and machineType and machineNum from session
       Find machine using API
       If machine is available, tell user
       If not, offer to set a timer
    """
    if session.get('user'):
        userId = session.get('user').get('userId')
        response = table.get_item(Key = {'userId': userId})
        
        if response.get('Item'):
            buildingId = response.get('Item').get('buildingId')
            machineType = intent.get('slots').get('machineType').get('value')
            machineNum = intent.get('slots').get('machineNum').get('value')
            
            """Format number"""
            machineId = buildingId + '-' + machineType + '-' + str(machineNum).zfill(2)
            
            """Call API buildings/buildingId/machines/machineId"""
            machineInfo = callApi(
                url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines/{}'
                .format(buildingId, machineId)
            )
            
            """If machine exists"""
            if type(machineInfo) == list:
                status = machineInfo.get('status')
                if status == 'available':
                    speechOutput = 'That {} is available.'.format(machineType)
                    repromptText = 'That {} is available.'.format(machineType)
                else:
                    timeLeft = machineInfo.get('timeLeft')
                    speechOutput = 'That {} is not available. There are {} minutes remaining.'\
                                   ' I can let you know when it is available if you say, '\
                                   'let me know when that {} is available'.format(machineType,timeLeft, machineType)
                    repromptText = 'I can let you know when a {} is available if you say, '\
                                   'let me know when a {} is available.'.format(machineType, machineType)
            else:
                """Machine not found"""
                speechOutput = 'I could not find that {}.'\
                               'You can tell me the {} by saying, is {} number x available.'.format(machineType, machineType, machineType)
                repromptText = 'You can tell me the {} by saying, is {} number x available.'.format(machineType, machineType)           
        
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
