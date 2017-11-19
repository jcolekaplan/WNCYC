""" --------------- Helpers that build all of the responses ---------------------- """
def buildSpeechletResponse(title, output, repromptText, shouldEndSession):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': repromptText
            }
        },
        'shouldEndSession': shouldEndSession
    }

def buildResponse(sessionAttributes, speechletResponse):
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttributes,
        'response': speechletResponse
    }

""" --------------- Functions that control the skill's behavior ------------------ """
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

def handleSessionEndRequest():
    cardTitle = 'Session Ended'
    speechOutput = 'Thank you for trying the Why Not Change Your Clothes? Alexa skill demo.' \
                    'Have a nice day! '
    """Setting this to true ends the session and exits the skill."""
    shouldEndSession = True
    return buildResponse({}, buildSpeechletResponse(
        cardTitle, speechOutput, None, shouldEndSession))

def createBuildingAttributes(building):
    return {'building': building}

def setBuildingInSession(intent, session):
    """ Sets the building in the session and prepares the speech to reply to the user."""
    cardTitle = intent.get('name')
    sessionAttributes = {}
    shouldEndSession = False

    if 'building' in intent.get('slots'):
        building = intent.get('slots').get('building').get('value')
        sessionAttributes = createBuildingAttributes(building)
        speechOutput = 'I now know your building is ' + building.capitalize() + '. ' \
                       'You can ask me what your building is by saying, what is my building?'
        repromptText = 'You can ask me what your building is by saying, what is my building?'
    else:
        speechOutput = 'I am not sure what your building is. Please try again.'
        repromptText = 'I am not sure what your building is. Please try again.' \
                       'You can tell me your building by saying, my building is.'
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        cardTitle, speechOutput, repromptText, shouldEndSession))

def getBuildingFromSession(intent, session):
    sessionAttributes = {}
    repromptText = None

    if session.get('attributes', {}) and 'building' in session.get('attributes', {}):
        building = session.get('attributes').get('building')
        speechOutput = 'Your building is ' + building + '. Goodbye.'
        shouldEndSession = True
    else:
        speechOutput = 'I am not sure what your building is. Please try again.' \
                       'You can tell me your building by saying, my building is.'
        shouldEndSession = False
     
    """Setting repromptText to None signifies that we do not want to reprompt
       the user. If the user does not respond or says something that is not
       understood, the session will end.
    """   
    return buildResponse(sessionAttributes, buildSpeechletResponse(
        intent.get('name'), speechOutput, repromptText, shouldEndSession))

""" --------------- Events ------------------ """
def onSessionStarted(sessionStartedRequest, session):
    """ Called when the session starts """
    print('onSessionStarted requestId=' + sessionStartedRequest.get('requestId')
          + ', sessionId=' + session.get('sessionId'))

def onLaunch(launchRequest, session):
    """ Called when the user launches the skill without specifying what they
        want
    """
    print('onLaunch requestId=' + launchRequest.get('requestId') +
          ', sessionId=' + session.get('sessionId'))
    return getWelcomeResponse()

def onIntent(intentRequest, session):
    """ Called when the user specifies an intent for this skill """
    
    print('onIntent requestId=' + intentRequest.get('requestId') +
          ', sessionId=' + session.get('sessionId'))

    intent = intentRequest.get('intent')
    intentName = intentRequest.get('intent').get('name')

    """ Dispatch to skill's intent handlers """
    if intentName == 'MyBuildingIsIntent':
        return setBuildingInSession(intent, session)
    elif intentName == 'WhatsMyBuildingIntent':
        return getBuildingFromSession(intent, session)
    elif intentName == 'AMAZON.HelpIntent':
        return getWelcomeResponse()
    elif intentName == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handleSessionEndRequest()
    else:
        raise ValueError('Invalid intent')

def onSessionEnded(sessionEndedRequest, session):
    """ Called when the user ends the session.
        Is not called when the skill returns shouldEndSession=True
    """
    print('onSessionEnded requestId=' + sessionEndedRequest.get('requestId') +
          ', sessionId=' + session.get('sessionId'))

""" --------------- Main handler ------------------ """

def lambdaHandler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
        etc.) The JSON body of the request is provided in the event parameter.
    """
    print('event.session.application.applicationId=' +
          event.get('session').get('application').get('applicationId'))

    """
    if (event.get('session').get('application').get('applicationId') !=
         'amzn1.echo-sdk-ams.app..get(unique-value-here)'):
         raise ValueError('Invalid Application ID')
    """
    if event.get('session').get('new'):
        onSessionStarted({'requestId': event.get('request').get('requestId')}, event.get('session'))

    if event.get('request').get('type') == 'LaunchRequest':
        return onLaunch(event.get('request'), event.get('session'))
    elif event.get('request').get('type') == 'IntentRequest':
        return onIntent(event.get('request'), event.get('session'))
    elif event.get('request').get('type') == 'SessionEndedRequest':
        return onSessionEnded(event.get('request'), event.get('session'))
