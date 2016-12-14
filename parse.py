import sys
import re
import jsonpickle

from common import *
from generate import check
from programs import program0

patternDriver = r'Driver\(([^,]*),([^,]*),([^,]*),([^,]*)\)'
patternRoad = r'Road\(([^,]*),([^,]*),([^,]*),([^,]*)\)'

def parse(inputFile,outputFile):
	env=Crossroad()	
	for line in inputFile.readlines():
		res = re.match(patternDriver,line.strip())
		# This line describes a driver
		if(res != None):
			name=res.group(1)
			current_road=res.group(2)
			destination_group=res.group(3)
			if(res.group(4)=='true'):
				emergency=True
			else:
				emergency=False
			env.add_thing(Driver(program0,name,current_road,destination_group,emergency))

		res = re.match(patternRoad,line.strip())
		# This line describes a road
		if(res != None):
			name=res.group(1)
			leftName=res.group(2).strip()
			if (leftName == ''):
				left=[]
			else:
				left=[leftName]

			forwardName=res.group(3).strip()
			if (forwardName == ''):
				forward=[]
			else:
				forward=[forwardName]

			rightName=res.group(4).strip()
			if (rightName == ''):
				right=[]
			else:
				right=[rightName]

			env.add_thing(Road(name,left,forward,right))
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