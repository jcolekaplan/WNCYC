"""Intents"""
from setBuildingIntent import *
from getWelcomeResponseIntent import *
from handleSessionEndRequestIntent import *

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
def alexaHandler(event, context):
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
