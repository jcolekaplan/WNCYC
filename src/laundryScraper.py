"""Libraries for reading in webpages and parsing them"""
import urllib3
from bs4 import BeautifulSoup

"""Include building and machine classes"""
from building import *
from machine import *

"""Read in the LaundryView page for Barton Hall then use BeautifulSoup to convert it into a parsable object"""
http = urllib3.PoolManager()
barton = http.request('GET', 'http://classic.laundryview.com/classic_laundry_room_ajax.php?lr=3695891&adk=155604%27')
soup = BeautifulSoup(barton.data, 'html.parser')

"""Finds each row of the table with all the info for the given laundry room
   Puts each row in a list
"""
table = soup.find_all('tr')

"""Will hold all machines of type Machine once info is parsed"""
bartonMachines = []

"""Go through each row of the table
   If the row contains div class="desc", then that row contains the machineNum, extract it
   If the row contains alt="inuse" or alt="available" then it contains a .gif with the correct machineType, extract it
   If the row contains div class="runtime", extract the runtime
   Then, using all that info, create a Machine object, at it to Barton's list of machines
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
            runTimeInt = [int(s) for s in runTime.split() if s.isdigit()]
        else:
            runTimeInt = 0
            
        machineId = machineType + '-' + machineNum
        buildingId = 'Barton Hall-2 Floor'
        if sum(p.machineId == machineId for p in bartonMachines) == 0:
            bartonMachines.append(Machine(runTime, machineId, buildingId, machineType, runTimeInt, True))

"""Get the relevant info for Barton then create a Building object with all that info"""
numWashers = sum(p.machineType == 'Washer' for p in bartonMachines)
numDryers = sum(p.machineType == 'Dryer' for p in bartonMachines)
nameList = ['Barton', 'Barton Hall', 'Hotel Barton']
Barton = Building('success', 'Barton Hall-2 Floor', nameList, numWashers, numDryers)

for machine in bartonMachines:
    print (machine.machineId + ': ', machine.status)
