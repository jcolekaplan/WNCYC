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
            buildingId = APIBuildingId(response)
            machineType = APIMachineType(intent)
            numMachinesRequested = APINumMachinesRequested(intent)
            
            """API Call /buildings/buildingId/machineType=machineType"""
            totalMachines = APIInfo(buildingId, machineType, False, "")
            numTotalMachines = len(totalMachines)
            
            """API Call /buildings/buildingId/machines?=available&machineType=machineType"""
            machineInfo = APIInfo(buildingId, machineType, True, "")
            
            numAvailMachines = len(machineInfo)
            """More available machines than requested machines"""
            if type(machineInfo) == list and (numAvailMachines >= numMachinesRequested):
                speechOutput, repromptText = machinesAvail(numAvailMachines, machineType)
            """More machines requested than exist in the building"""
            elif numTotalMachines < numMachinesRequested:
                speechOutput, repromptText = tooManyMachines(numTotalMachines, machineType)
            """More machines requested than are available"""
            else:
               speechOutput, repromptText = settingMulTimers(numMachinesRequested, machineType, totalMachines)
        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()

    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))