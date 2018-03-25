import boto3
from utils import *
from boto3.dynamodb.conditions import Key, Attr

"""Dynamo resource and table"""
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Users')

def setMachineTimer(intent, session):

    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False
    
    """Get buildingId from User table and machineType and machineNum from session
       Get machine info using API
       If machine is available, tell user
       If not, set a timer
    """
    if session.get('user'):
        userId = session.get('user').get('userId')
        response = table.get_item(Key = {'userId': userId})
        
        if response.get('Item'):
            buildingId = APIBuildingId(response)
            machineType = APIMachineType(intent)
            machineNum = APIMachineNum(intent)
            
            """Format number"""
            machineId = buildingId + '-' + machineType + '-' + str(machineNum).zfill(2)
            
            """Call API /buildings/buildingId/machines/machineId"""
            machineInfo = APIInfo(buildingId, machineType, False, machineId)
            
            """If API call successful"""
            if not machineInfo.get('error'):
                """And machine is available"""
                if machineInfo.get('status') == 'available':
                    speechOutput, repromptText = thatMachineIsAvail(machineType)
                """And machine is not available"""
                else:
                    speechOutput, region_name = settingATimer(machineType, machineInfo.get('timeLeft'))
            else:
                speechOutput, repromptText = machineNotFound(machineType)
        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()

    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))