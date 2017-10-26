import urllib3
from bs4 import BeautifulSoup

"""Include building and machine classes"""
from buildingsInfo import *
from building import *
from machine import *

"""Read in the LaundryView page for Barton Hall then use BeautifulSoup to convert it into a parsable object"""
http = urllib3.PoolManager()
url = 'http://classic.laundryview.com/classic_laundry_room_ajax.php?lr={}'

"""Used to store Building and Machine objects with all the relevant info"""
buildingList = list()
machineDict = dict()

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
				machineType = 'Washer'
			else:
				machineType = 'Dryer'
				
		if row.find('div', 'runtime'):
			runTime = row.find('div', 'runtime').get_text().strip()
			if runTime.find('remaining') != -1:
				runTimeInt = [int(s) for s in runTime.split() if s.isdigit()][0]
			else:
				runTimeInt = 0
				
			machineId = machineType + '-' + machineNum		
			if machineId not in foundMachines:
				foundMachines.add(machineId)
				machineDict[buildingId].append((Machine(runTime, machineId, buildingId, machineType, runTimeInt, True)))
	
	"""Using data found above, create Building object
	   Store in buildingList
	"""
	numWashers = sum(p.machineType == 'Washer' for p in machineDict[buildingId])
	numDryers = sum(p.machineType == 'Dryer' for p in machineDict[buildingId])
	buildingList.append(Building('success', buildingId, buildingInfo['friendlyNames'], numWashers, numDryers))

"""Test"""
for building in buildingList:
	print('\n{} #Washers={} #Dryers={}'.format(building.buildingId, building.numWashers, building.numDryers))
	for machine in machineDict[building.buildingId]:
		print('{}: {}'.format(machine.machineId, machine.status))
