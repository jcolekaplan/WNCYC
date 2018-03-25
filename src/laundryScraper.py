import boto3
import urllib3

from bs4 import BeautifulSoup

"""Include building and machine classes"""
from machine import *
from building import *
from buildingsInfo import *
from DynamoTable import *


def handler(event, context):
    """Client with access keys to write to Dynamo tables online"""
    buildingTable = DynamoTable('Buildings')
    machineTable = DynamoTable('Machines')
    return scrapeLaundry(event, context, buildingTable, machineTable)
    
"""Scrape LaundryView for each building and all machines in each building
   Put all the info into Building and Machine objects
   Put all those objects into buildingList and machineDict
"""   
def scrapeLaundry(event, context, buildingTable, machineTable):
    
    """Used to store Building and Machine objects with all the relevant info"""
    buildingList = list()
    machineDict = dict()

    """Read in the LaundryView page for building then use BeautifulSoup to convert it into a parsable object"""
    http = urllib3.PoolManager()
    url = 'http://classic.laundryview.com/classic_laundry_room_ajax.php?lr={}'
    
    """Go through the buildings listed in buildingsInfo.py"""
    for buildingInfo in buildingsInfo:
        """Format correct URL and reads in web-page"""
        laundryRoom = buildingInfo['roomNum']
        building = http.request('GET', url.format(laundryRoom))
        soup = BeautifulSoup(building.data, 'html.parser')
    
        """Finds each row of the table with all the info for the given laundry room
           Puts each row in a list
        """
        table = soup.find_all('tr')
        
        """Will use to check for machine duplicates"""
        foundMachines = set()
        
        """Initializes list of machines in that building"""
        buildingId = buildingInfo['buildingId']
        machineDict[buildingId] = list()
    
        """Go through each row of the table
           If the row contains div class="desc", then that row contains the machineNum, extract it
           If the row contains alt="inuse" or alt="available" then it contains a .gif with the correct machineType, extract it
           If the row contains div class="runtime", extract the runtime
           Then, using all that info, create a Machine object, add it to the list of machines with key corresponding to buildingId
        """
        countMachineNotFound = 0
        for row in table:
            if row.find('td', 'bgicon'):
                findMachineType = row.find(alt={'inuse', 'available'})
                if str(findMachineType).find('washer') != -1:
                    machineType = 'washer'
                elif str(findMachineType).find('dryer') != -1:
                    machineType = 'dryer'
                
            if row.find('td', 'bgdesc'):
                machineNum = row.find('div','desc').get_text().strip()
                
                if machineNum == '':
                    countMachineNotFound += 1
                    machineNum = 'notFound{}'.format(countMachineNotFound)
                
                
            if row.find('div', 'runtime'):
                runTime = row.find('div', 'runtime').get_text().strip()
                if runTime.find('remaining') != -1:
                    runTimeInt = [int(s) for s in runTime.split() if s.isdigit()][0]
                elif runTime.find('out of service') != -1:
                    runTimeInt = -1
                elif runTime.find('unknown') != -1:
                    runTimeInt = -1
                elif runTime.find('closed') != -1:
                    runTimeInt = -1
                else:
                    runTimeInt = 0
            
                machineId = buildingId + '-' + machineType + '-' + machineNum
                if machineId not in foundMachines:
                    foundMachines.add(machineId)
                    machineDict[buildingId].append((Machine(runTime, machineId, buildingId, machineType, runTimeInt)))

        """If machine has notFoundX as its number,
           Iterate through numbers 01 to XX until it finds one that's not taken,
           and assign it to that machine.
        """
        tryMachineNum = 1
        for machines in machineDict[buildingId]:
            while machines.machineId.find('notFound') != -1:
                tryMachineNumStr = str(tryMachineNum).zfill(2)
                tryMachineId = machines.buildingId + '-' + machines.machineType + '-' + tryMachineNumStr
                
                if tryMachineId not in foundMachines:
                    machines.machineId = tryMachineId
                    foundMachines.add(tryMachineId)
                    break
                else:
                    tryMachineNum += 1
        
        """Using data found above, create Building object
           Store in buildingList
        """
        numWashers = sum(p.machineType == 'washer' for p in machineDict[buildingId])
        numDryers = sum(p.machineType == 'dryer' for p in machineDict[buildingId])
        buildingList.append(Building(buildingId, buildingInfo['friendlyNames'], numWashers, numDryers))
        
    """Call writeDynamo to re-format buildingList and machineDict and write to Dynamo table"""
    writeDynamo(buildingList, machineDict, buildingTable, machineTable)
    
"""Iterate through buildingList and machineDict
   Convert to dynamo format and write info to table
"""
def writeDynamo(buildingList, machineDict, buildingTable, machineTable):

    """Go through each building, convert it to dictionary, and put in relevant info in    
       Dynamo format
       Go through the machines for each of those buildings, do the same
       Then, write buildingTable and machineTable to Dynamo table
    """
    for building in buildingList:
        buildingTable.putItem(building)

        for machine in machineDict[building.buildingId]:
            if machine.timeLeft != -1:
                machineTable.putItem(machine)