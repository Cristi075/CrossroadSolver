import sys
import re
import jsonpickle

from common import *
from generate import check
from programs import program0

patternDriver = r'Driver\(([^,]*),([^,]*),([^,]*),([^,]*)\)'
patternRoad = r'Road\(([^,]*),([^,]*),([^,]*),([^,]*)\)'
patternSign = r'Sign\(([^,]*),([^,]*)\)'

def parse(inputFile,outputFile):
	env=Crossroad()	
	for line in inputFile.readlines():
		resDriver 	= re.match(patternDriver,line.strip())
		resRoad   	= re.match(patternRoad,line.strip())
		resSign		= re.match(patternSign,line.strip())
		if(resDriver != None): # This line describes a driver
			name=resDriver.group(1)
			current_road=resDriver.group(2)
			destination_group=resDriver.group(3)
			if(resDriver.group(4)=='true'):
				emergency=True
			else:
				emergency=False
			env.add_thing(Driver(program0,name,current_road,destination_group,emergency))
		elif(resRoad != None): # This line describes a road
			name=resRoad.group(1)
			leftName=resRoad.group(2).strip()
			if (leftName == ''):
				left=[]
			else:
				left=[leftName]

			forwardName=resRoad.group(3).strip()
			if (forwardName == ''):
				forward=[]
			else:
				forward=[forwardName]

			rightName=resRoad.group(4).strip()
			if (rightName == ''):
				right=[]
			else:
				right=[rightName]

			env.add_thing(Road(name,left,forward,right))
		elif(resSign != None):
			name=resSign.group(1)
			road=resSign.group(2)
			env.add_thing(Sign(name,road))
		else:
			if(line.strip()!=''):
				print('The following line did not match any of the existing patterns:')
				print(line)
	inputFile.close()
	print('Environment created. Running checks')
	if(check(env)):
		print('The created environment is valid')
		print('Writing the environment to '+outputFile.name)
		outputFile.write(jsonpickle.encode(env))
		outputFile.close()
	else:
		print('The created environment is invalid')
		outputFile.close()