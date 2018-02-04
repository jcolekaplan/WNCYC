from utils import *

def handleSessionEndRequest():
    cardTitle = 'Session Ended'
    speechOutput = 'Thank you for trying the Why Not Change Your Clothes? Alexa skill demo.' \
                    'Have a nice day! '
    """Setting this to true ends the session and exits the skill."""
    shouldEndSession = True
    return buildResponse({}, buildSpeechletResponse(
        cardTitle, speechOutput, None, shouldEndSession))