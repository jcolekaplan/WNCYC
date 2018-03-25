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
    
"""--------------- Helpers to format the responses ---------------"""
"""Finds machine with nth lowest time"""
def nLowestTime(n, machines):
    sortedMachines = sorted(machines, key=lambda x: x.get('timeLeft'))
    return sortedMachines[n-1].get('timeLeft')

"""Grammatical functions"""
def isOrAre(numAvailMachines):
    if numAvailMachines == 1:
        return "is"
    else:
        return "are"
        
def isPlur(numAvailMachines):
    if numAvailMachines == 1:
        return ""
    else:
        return "s"
"""Tells user their building"""
def yourBuildingIs(building):
    speechOutput = 'Your building is {}. '\
                   'You can hear your building name again by saying, '\
                   'what is my building?'.format(building)
    repromptText = 'You can hear your building name again by saying, what is my building?'
    return speechOutput, repromptText

"""Machine requested is available"""
def thatMachineIsAvail(typ):
    speechOutput = 'That {} is available.'.format(typ)                   
    repromptText = 'That {} is available.'.format(typ)
    return speechOutput, repromptText

"""Tells user how many machines of that type are available now"""
def machinesAvail(num, typ):
    isAre = isOrAre(num)
    plur = isPlur(num)
    speechOutput = 'There {} {} available {}{} in your building right now'\
                    .format(isAre, num, typ, plur)
    repromptText = 'There {} {} available {}{} in your building right now'\
                    .format(isAre, num, typ, plur)
    return speechOutput, repromptText

"""Tells user the number of machines requested exceeds the number of machines in their building"""
def tooManyMachines(num, typ):
    isAre = isOrAre(num)
    plur = isPlur(num)
    speechOutput = 'There {} only {} {}{} in your building.'\
                    .format(isAre, num, typ, plur)
    repromptText = 'There {} only {} {}{} in your building.'\
                    .format(isAre, num, typ, plur)
    return speechOutput, repromptText

"""More machines requested than available, offers to set timer"""
def notEnoughAvail(numA, numR, typ):
    isAreA = isOrAre(numA)
    isAreR = isOrAre(numR)
    plurA = isPlur(numA)
    plurR = isPlur(numR)
    speechOutput = 'There {} only {} available {}{} in your building right now. ' \
                   'I can set a timer if you say, let me know when {} {}{} {} available'\
                   .format(isAreA, numA, typ, plurA, numR, typ, plurR, isAreR)

    repromptText =  'I can set a timer if you say, let me know when {} {}{} {} available'\
                   .format(isAreA, numA, typ, plurA, numR, typ, plurR, isAreR)
    return speechOutput, repromptText
    
"""No machines available"""
def noAvailMachines(typ):
    speechOutput = 'There are no available {}s in your building right now.'\
                   'I can let you know when one is available if you say, '\
                   'let me know when a {} is available.'\
                   .format(typ, typ)
    repromptText = 'I can let you know when a {} is available if you say, '\
                   'let me know when a {} is available.'\
                   .format(typ, typ) 
    return speechOutput, repromptText

"""Machine requested had x time left"""
def thatMachineHasTimeLeft(typ, time):
    speechOutput = 'That {} is not available. There are {} minutes remaining.'\
                   ' I can let you know when it is available if you say, '\
                   'let me know when that {} is available'\
                   .format(typ, time, typ)
    repromptText = 'I can let you know when a {} is available if you say, '\
                   'let me know when a {} is available.'\
                   .format(typ, typ)
    return speechOutput, repromptText

"""Response when skill sets a timer for a single machine"""
def settingATimer(typ, time):
    speechOutput = 'Setting a timer. There are {} minutes remaining.'\
                   ' I will let you know when that {} is available'.format(time, typ)
    repromptText = 'There are {} minutes remaining.'\
                   ' I will let you know when that {} is available'.format(time, typ)
    return speechOutput, repromptText

"""Response when skill sets a timer for multiple machines"""
def settingMulTimers(numR, typ, mach):
    numL = nLowestTime(numR, mach)
    plur = isPlur(numR)
    speechOutput = 'Setting a timer. {} {}{} will be available in {} minutes. '\
                    'I will let you know when the timer is done.'\
                   .format(str(numR), typ, plur, numL)
    repromptText = '{} {}{} will be available in {} minutes.'\
                   .format(str(numR), typ, plur, numL)
    return speechOutput, repromptText

"""Not found responses ------------------"""
def machineNotFound(typ):
    speechOutput = 'I could not find that {}. '\
                   'You can tell me the {} by saying, is {} number x available.'\
                   .format(typ, typ, typ)
    repromptText = 'You can tell me the {} by saying, is {} number x available.'\
                   .format(typ, typ)           
    return speechOutput, repromptText
    
def buildingNotFound():
    """No valid building for user in User table"""
    speechOutput = 'I could not find your building. '\
                   'You can tell me your building by saying, my building is.'
    repromptText = 'You can tell me your building by saying, my building is.'
    return speechOutput, repromptText

def userNotFound():
    """No user with that ID found in User table"""
    speechOutput = 'I am sorry. I do not know what your building is. '\
                   'You can tell me your building by saying, my building is.'
    repromptText = 'You can tell me your building by saying, my building is.'
    return speechOutput, repromptText

"""Weclome response"""
def welcomeResponse():
    speechOutput = 'Welcome to the Why Not Change Your Clothes? Alexa skill demo.' \
                    'Please tell me your building.' \
                    'You can tell me your building by saying, my building is.'
    repromptText = 'Please tell me your building.' \
                   'You can tell me your building by saying, my building is.'
    return speechOutput, repromptText

"""End response"""
def endResponse():
    speechOutput = 'Thank you for trying the Why Not Change Your Clothes? Alexa skill demo.' \
                    'Have a nice day! '
    repromptText = 'Thank you for trying the Why Not Change Your Clothes? Alexa skill demo.' \
                    'Have a nice day! '
    return speechOutput, repromptText
    
""" --------------- Get info from API ------------- """
def APIInfo(buildingId, machineType, getAvail, machineId):
    if machineId != "":
        url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines/{}'\
                .format(buildingId, machineId)
    elif machineId == "" and getAvail == True:
        url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines?status=available&machineType={}'\
                .format(buildingId, machineType)
    else:
        url = 'https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings/{}/machines?machineType={}'\
                .format(buildingId, machineType)
    return callApi(url)

def APIFindBuilding(friendlyName):
    url = "https://go3ba09va5.execute-api.us-east-2.amazonaws.com/Test/buildings?friendlyName={}".format(friendlyName).replace(' ', '%20')
    return callApi(url)

def APIBuilding(intent):
    return intent.get('slots').get('building').get('value')
    
def APIBuildingId(response):
    return response.get('Item').get('buildingId')

def APIMachineType(intent):
    return intent.get('slots').get('machineType').get('value').strip('s')

def APIMachineNum(intent):
    return intent.get('slots').get('machineNum').get('value')
    
def APINumMachinesRequested(intent):
    numMachinesRequested = 1
    if intent.get('slots').get('numMachines').get('value'):
        numMachinesRequested = intent.get('slots').get('numMachines').get('value')
    return int(numMachinesRequested)

def callApi(url):
       http = urllib3.PoolManager()
       r = http.request('GET', url)
       data = r.data
       print(url)
       jsonData = json.loads(data)
       return jsonData