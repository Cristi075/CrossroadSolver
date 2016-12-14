from common import *
from programs import program0
import jsonpickle


min_roads=2
max_roads=4

# This function will be called if a road is referenced but it is not defined
# Parameters: 
# road = The name of the road that was not found
# refAt = The name of the road/driver that has the wrong reference
# place = where is it referenced. It will be left/forward/right for a road or current/destination for a driver
def road_not_found_message(road,refAt,place):
	print('ERROR: Road not found')
	print('Road '+road+' referenced at '+refAt+' '+place+' does not exist')

# Checks if a list has a duplicate.
# If duplicates are found it will print an error and return true 
# If no duplicates are found no error is printed and the function returns false
# The place parameter is a name that should tell the user what list contains duplicates
def check_for_duplicates(list,place):
	if(len(list) != len(set(list))):
		print('ERROR: Duplicated names found at '+place)
		print('List:'+str(list))
		return True # duplicates exist
	return False

def check(env):
	roads= [thing for thing in env.things if isinstance(thing,Road)]
	road_names= [road.name for road in roads]
	
	# The environmnet is not valid if there are two roads with the same name
	if(check_for_duplicates(road_names,'road names list')):
		return False

	for road in roads:
		all_connections=road.left+road.forward+road.right

		# The environmnet is not valid  if a road has two connections with the same road
		if(check_for_duplicates(all_connections,road.name+' \'s connections')):
			return False

		for connected_road in road.left:
			#The environmnet is not valid if the name of a connection does not exist
			if connected_road not in road_names:
				road_not_found_message(connected_road,road.name,'left')
				return False

			#The environmnet is not valid if a road has a connection with itself
			if connected_road == road.name:
				print('ERROR: Road '+road.name+ ' connected with itself (left)')
				return False

		for connected_road in road.forward:
			#The environmnet is not valid if the name of a connection does not exist
			if connected_road not in road_names:
				road_not_found_message(connected_road,road.name,'forward')
				return False

			#The environmnet is not valid if a road has a connection with itself
			if connected_road == road.name:
				print('ERROR: Road '+road.name+ ' connected with itself (forward)')
				return False

		for connected_road in road.right:
			#The environmnet is not valid if the name of a connection does not exist
			if connected_road not in road_names:
				road_not_found_message(connected_road,road.name,'right')
				return False

			#The environmnet is not valid if a road has a connection with itself
			if connected_road == road.name:
				print('ERROR: Road '+road.name+ ' connected with itself (right)')
				return False

	agents=[thing for thing in env.things if isinstance(thing,Agent)]	
	for agent in agents:
		# Check if every initial road exists
		if agent.current_road not in road_names:
			road_not_found_message(agent.current_road,agent.name,'current_road')
			return False

		# Check if every target road exists
		if agent.destination_road not in road_names:
			road_not_found_message(agent.current_road,agent.name,'destination_road')
			return False

	# Check for duplicated agent names
	agent_names= [agent.name for agent in agents]
	if(check_for_duplicates(agent_names,'agent names list')):
		return False

	# The environment is not valid if we have two agents starting from the same road
	initial_roads= [agent.current_road for agent in agents]
	if(check_for_duplicates(initial_roads,'current_road names list')):
		return False

	# If every test passed we return true confirming that the environment is valid
	return True


def generate():
	roads=[]
	drivers=[]

	nr_of_roads=-1
	while(nr_of_roads==-1):
		nr_of_roads=int(input('Number of roads:'))

		if(nr_of_roads > max_roads):
			print('ERROR: Maximum number of roads is '+str(max_roads))
			nr_of_roads=-1
		elif(nr_of_roads < min_roads):
			print('ERROR: Minimum number of roads is '+str(min_roads))
			nr_of_roads=-1

	print('You will be prompted to enter the details for each road')
	print('Please use consistent naming when entering the names of the connected roads')
	print('If a connection does not exist just press enter')

	env=Crossroad()
	for i in range(1,nr_of_roads+1):
		print('Road nr.'+str(i))
		roadName=input('Name:')
		print('Enter the names of the roads that are connected to this one')

		leftName=input('Left:')
		if(leftName==''):
			left=[]
		else:
			left=[leftName]

		forwardName=input('Forward:')
		if(forwardName==''):
			forward=[]
		else:
			forward=[forwardName]

		rightName=input('Right:')
		if(rightName==''):
			right=[]
		else:
			right=[rightName]

		env.add_thing(Road(roadName,left,forward,right))


	nr_of_drivers=-1
	while(nr_of_drivers==-1):
		nr_of_drivers=int(input('Number of drivers:'))

		if(nr_of_drivers > nr_of_roads):
			print('ERROR: Maximum number of drivers is '+str(nr_of_roads))
			nr_of_drivers=-1
		elif(nr_of_drivers < 1):
			print('ERROR: Minimum number of drivers is '+str(1))
			nr_of_drivers=-1

	print('You will be prompted to enter the details for each driver')

	for i in range(1,nr_of_drivers+1):
		print('Driver nr.'+str(i))
		driverName=input('Name:')

		sourceName=''
		while(sourceName==''):
			sourceName=input('Initial road:')
			if (sourceName == ''):
				print("ERROR: Blank names are not allowed. Try again")

		destName=''
		while(destName==''):
			destName=input('Target road:')
			if (destName == ''):
				print("ERROR: Blank names are not allowed. Try again")


		print('Is this an emergency vehicle? (y/n)')
		emergencyInput=input('>')
		if(emergencyInput=='y'):
			emergency=True
		else:
			emergency=False

		env.add_thing(Driver(program0,driverName,sourceName,destName,emergency))


	if(check(env)):
		return env
	else:
		return None