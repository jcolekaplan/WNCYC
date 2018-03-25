from utils import *

def handleSessionEndRequest():
    cardTitle = 'Session Ended'
    shouldEndSession = True
    speechOutput, repromptText = endResponse()
    return buildResponse({}, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))