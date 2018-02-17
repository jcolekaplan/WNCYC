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
            buildingId = APIBuildingId(response)
            machineType = APIMachineType(intent)
            numMachinesRequested = APINumMachinesRequested(intent)
            
            """API Call /buildings/buildingId/machineType=machineType"""
            totalMachines = APIInfo(buildingId, machineType, False, "")
            numTotalMachines = len(totalMachines)
            
            """API Call /buildings/buildingId/machines?=available&machineType=machineType"""
            machineInfo = APIInfo(buildingId, machineType, True, "")
            
            numAvailMachines = len(machineInfo)
            """More machines available than requested"""
            if type(machineInfo) == list and (numAvailMachines >= numMachinesRequested):
                speechOutput, repromptText = machinesAvail(numAvailMachines, machineType)
            """More machines requested than exist in building"""
            elif numTotalMachines < numMachinesRequested:
                speechOutput, repromptText = tooManyMachines(numTotalMachines, machineType)
            """More machines requested than available but some are available"""
            elif numAvailMachines > 0 and numAvailMachines < numMachinesRequested:
                speechOutput, repromptText = notEnoughAvail(numAvailMachines, numMachinesRequested, machineType)
            """No machines available"""
            else:
                speechOutput, repromptText = noAvailMachines(machineType)
        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()
        
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))