import boto3
from utils import *
from dynamoTable import *
from boto3.dynamodb.conditions import Key, Attr

def getAvailMachines(intent, session):
    """Dynamo resource"""
    userTable = DynamoTable('Users')
    return buildAvailMachinesResponse(intent, session, userTable)
    
def buildAvailMachinesResponse(intent, session, userTable):
    
    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False

    """Get buildingId from User table and machineType from session
       Get available machines using API
       If there are available machines, tell user how many
       If not, offer to set a timer
    """
    if session.get('user'):
        userIdVal = session.get('user').get('userId')
        response = userTable.get(userId=userIdVal)
        
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
            elif numTotalMachines < numMachinesRequested:
                speechOutput, repromptText = tooManyMachines(numTotalMachines, machineType)
            elif numAvailMachines > 0 and numAvailMachines < numMachinesRequested:
                speechOutput, repromptText = notEnoughAvail(numAvailMachines, numMachinesRequested, machineType)
            else:
                speechOutput, repromptText = noAvailMachines(machineType)
        else:
            speechOutput, repromptText = buildingNotFound()
    else:
        speechOutput, repromptText = userNotFound()
        
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))