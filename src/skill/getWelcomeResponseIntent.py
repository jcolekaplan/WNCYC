from utils import *

def getWelcomeResponse():
    sessionAttributes = {}
    cardTitle = 'Welcome'
    speechOutput = 'Welcome to the Why Not Change Your Clothes? Alexa skill demo.' \
                    'Please tell me your building.' \
                    'You can tell me your building by saying, my building is.'
    
    """If the user either does not reply to the welcome message or says something
       that is not understood, they will be prompted again with this text.
    """
    repromptText = 'Please tell me your building.' \
                   'You can tell me your building by saying, my building is.'
    shouldEndSession = False
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))