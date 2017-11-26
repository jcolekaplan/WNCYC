import json
import urllib3

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
    
""" --------------- Get info from API ------------- """
def callApi(url):
       http = urllib3.PoolManager()
       r = http.request('GET', url)
       data = r.data
       print(url)
       jsonData = json.loads(data)
       return jsonData