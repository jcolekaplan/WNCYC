from utils import *

def getWelcomeResponse():
    sessionAttributes = {}
    cardTitle = 'Welcome'
    shouldEndSession = False
    speechOutput, repromptText = welcomeResponse()
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))