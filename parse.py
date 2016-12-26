import sys
import re
import jsonpickle

from common import *
from check import check
from programs import program0

patternDriver1 = r'Driver\(([^,]*),([^,]*),([^,]*),([^,]*)\)'
patternDriver2 = r'Driver\(([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)\)'
patternRoad = r'Road\(([^,]*),([^,]*),([^,]*),([^,]*)\)'
patternSign = r'Sign\(([^,]*),([^,]*)\)'

def parse(inputFile,outputFile):
	env=Crossroad()	
	for line in inputFile.readlines():
		resDriver1 	= re.match(patternDriver1,line.strip())
		resDriver2 	= re.match(patternDriver2,line.strip())
		resRoad   	= re.match(patternRoad,line.strip())
		resSign		= re.match(patternSign,line.strip())
		if(resDriver1 != None): # This line describes a default driver (here, default refers to the yieldChance)
			name=resDriver1.group(1)
			current_road=resDriver1.group(2)
			destination_group=resDriver1.group(3)
			if(resDriver1.group(4)=='true'):
				emergency=True
			else:
				emergency=False
			env.add_thing(Driver(program0,name,current_road,destination_group,emergency))
		elif(resDriver2 != None): # This line describes a driver with a predefined yieldChance
			name=resDriver2.group(1)
			current_road=resDriver2.group(2)
			destination_group=resDriver2.group(3)
			if(resDriver2.group(4)=='true'):
				emergency=True
			else:
				emergency=False
			yieldChance=float(resDriver2.group(5))
			env.add_thing(Driver(program0,name,current_road,destination_group,emergency,yieldChance))
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