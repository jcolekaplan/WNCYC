import boto3
import urllib3
from bs4 import BeautifulSoup

"""Include building and machine classes"""
from machine import *
from building import *
from buildingsInfo import *

"""Convert all building and machine info to format compatible with DynamoDB tables"""
def dictToItem(raw):
	if type(raw) is dict:
		resp = {}
		for k,v in raw.items():
			if type(v) is str:
				resp[k] = {
				        'S': v
				}
			elif type(v) is int:
				resp[k] = {
				    'N': str(v)
				}
			elif type(v) is dict:
				resp[k] = {
				    'N': dictToItem(v)
				}
			elif type(v) is list:
				resp[k] = {'L': []}
				for i in v:
					resp[k]['L'].append(dictToItem(i))
		return resp

	elif type(raw) is str:
		return {
		        'S': raw
		}
	elif type(raw) is int:
		return {
		        'N': str(raw)
		}

"""Scrape LaundryView for each building and all machines in each building
   Put all the info into Building and Machine objects
   Put all those objects into buildingList and machineDict
"""   
def scrapeLaundry(event, context):
	
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
		for row in table:
			if row.find('div', 'desc'):
				machineNum = row.find('div','desc').get_text().strip()
				
			if row.find(alt={'inuse','available'}):
				machineType = row.find(alt={'inuse', 'available'})
				if str(machineType).find('washer') != -1:
					machineType = 'washer'
				else:
					machineType = 'dryer'
					
			if row.find('div', 'runtime'):
				runTime = row.find('div', 'runtime').get_text().strip()
				if runTime.find('remaining') != -1:
					runTimeInt = [int(s) for s in runTime.split() if s.isdigit()][0]
				elif runTime.find('out of service') != -1:
					runTimeInt = -1
				else:
					runTimeInt = 0
					
				machineId = buildingId + '-' + machineType + '-' + machineNum		
				if machineId not in foundMachines:
					foundMachines.add(machineId)
					machineDict[buildingId].append((Machine(runTime, machineId, buildingId, machineType, runTimeInt)))
		
		"""Using data found above, create Building object
		   Store in buildingList
		"""
		numWashers = sum(p.machineType == 'washer' for p in machineDict[buildingId])
		numDryers = sum(p.machineType == 'dryer' for p in machineDict[buildingId])
		buildingList.append(Building(buildingId, buildingInfo['friendlyNames'], numWashers, numDryers))
	
	"""Call writeDynamo to re-format buildingList and machineDict and write to Dynamo table"""
	writeDynamo(buildingList, machineDict)
	
"""Iterate through buildingList and machineDict
   Convert to dynamo format and write info to table
"""
def writeDynamo(buildingList, machineDict):
	"""Client with access keys to write to Dynamo tables online"""
	dynamodb = boto3.client('dynamodb', region_name = 'us-east-2')
	
	"""Go through each building, convert it to dictionary, and put in relevant info in    
	   Dynamo format
	   Go through the machines for each of those buildings, do the same
	   Then, write buildingTable and machineTable to Dynamo table
	"""
	for building in buildingList:
		
		buildingTable = dict()
		machineTable = dict()
		
		buildingTable['Buildings'] = list()
		machineTable['Machines'] = list()
		
		newBuilding = dict()
		newBuilding['PutRequest'] = dict()
		newBuilding['PutRequest']['Item'] = dictToItem(vars(building))
		buildingTable['Buildings'].append(newBuilding)
		
		for machine in machineDict[building.buildingId]:
			newMachine = dict()
			newMachine['PutRequest'] = dict()
			newMachine['PutRequest']['Item'] = dictToItem(vars(machine))
			machineTable['Machines'].append(newMachine)
	
		buildingResponse = dynamodb.batch_write_item(RequestItems=buildingTable)
		machineResponse = dynamodb.batch_write_item(RequestItems=machineTable)

if __name__ == '__main__':
	
	scrapeLaundry(None,None)
