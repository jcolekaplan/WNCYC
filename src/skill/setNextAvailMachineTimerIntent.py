import boto3
from utils import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource and table"""
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Users')

def setNextAvailMachineTimer(intent, session):

    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False
    
    """Get buildingId from User table and machineType from session
       Get available machines using API
       If there are available machines, tell user how many
       If not, set a timer for the next machine to become available
    """
    if session.get('user'):
        userId = session.get('user').get('userId')
        response = table.get_item(Key = {'userId': userId})
        
        if response.get('Item'):
            buildingId = response.get('Item').get('buildingId')
            machineType = intent.get('slots').get('machineType').get('value').strip('s')
            
            """Call API /buidlings/buildingId/machines?machineType=machineType&status=available"""
            machineInfo = callApi(
                url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines?status=available&machineType={}'
                .format(buildingId, machineType)
            )
            
            """Get number of available machines
               If it's non-zero, tell user how many there are
               If not, offer to set time for next available machine
            """
            numAvailMachines = len(machineInfo)
            if numAvailMachines > 0:
                speechOutput = 'There are {} available {}s in your building right now'.format(str(numAvailMachines), machineType)
                repromptText = 'There are {} available {}s in your building right now'.format(str(numAvailMachines), machineType)
            else:
                """Call API /buidlings/buildingId/machines?machineType=machineType
                   Find the next available machine
                """
                machineInfo = callApi(
                    url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines?machineType={}'
                    .format(buildingId, machineType)
                )
                lowestTimeLeft = 60
                for machine in machineInfo:
                    if 0 < machine.get('timeLeft') <= lowestTimeLeft:
                        lowestTimeLeft = machine.get('timeLeft')
                speechOutput = 'Setting a timer for the next available {} ' \
                               'The next available {} will be free in {} minutes. '\
                               'I will let you know when it is available.'.format(machineType, machineType, lowestTimeLeft)
                repromptText = 'The next available {} will be free in {} minutes. '\
                               'I will let you know when it is available.'.format(machineType, lowestTimeLeft)
        
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
