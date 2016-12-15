from common import *
from programs import program0
import jsonpickle

priority_signs	= [	'priority_road', 'priority_road_left', 'priority_road_right']
stop_signs		= [ 'stop', 'stop_left', 'stop_right' ]
valid_signs		= priority_signs + stop_signs

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

	signs= [thing for thing in env.things if isinstance(thing,Sign)]

	# Check if a sign is placed on an invalid road
	for sign in signs:
		if sign.road not in road_names:
			road_not_found_message(sign.road,sign.name,'sign\'s road')
			return False

		if sign.name not in valid_signs:
			print('ERROR: Invalid sign '+str(sign))
			return False

		other_signs=[s for s in signs if s.road==sign.road and s.name in valid_signs and s!=sign]
		if other_signs!=[]:
			print('ERROR: Multiple priority-related signs found on '+sign.road)
			return False


	nr_roads=len(roads)

	nr_priority=len([sign for sign in signs if sign.name in priority_signs])
	nr_stop=len([sign for sign in signs if sign.name in stop_signs])

	# We allow either two priority signs or none. Any other number is invalid
	if nr_priority!=0 and nr_priority!=2:
		print('ERROR: Invalid number of priority signs. 0 or 2 signs are allowed')
		return False

	if nr_stop>1 and nr_roads==3:
		print('ERROR: At most 1 stop sign is allowed for a 3-roads crossroad')
		return False
	else:
		if nr_stop!=0 and nr_stop!=2 and nr_roads>3:
			print('ERROR: Invalid number of stop signs. 0 or 2 signs are allowed on a 4-roads crossroad')
			return False


	# Check if the signs are placed correctly
	# Ex: 	If a priority road sign indicates that the priority road goes right
	# 		The road on the right should also have a priority road sign
	for sign in signs:
		# The road where this sign is placed
		sign_road=next(road for road in roads if road.name == sign.road)

		if sign.name=='priority_road':
			if sign_road.forward == None:
				print('ERROR: A priority_road sign is placed on a road with no forward connection')
				return False
			else:
				oposing_sign=[s for s in signs if s.road in sign_road.forward]
				if oposing_sign==[]: # Found no sign
					print('ERROR: Missing oposing sign for '+str(sign))
					print('Expected a priority_road sign on '+str(sign_road.forward))
					return False
				elif oposing_sign[0].name!='priority_road': # Found other sign
					print('ERROR: Wrong oposing sign for '+str(sign))
					print('Expected a priority_road sign on '+str(sign_road.forward))
					return False
		elif sign.name=='priority_road_right':
			if sign_road.right == None:
				print('ERROR: A priority_road_right sign is placed on a road with no right connection')
				return False
			else:
				oposing_sign=[s for s in signs if s.road in sign_road.right]
				if oposing_sign==[]: # Found no sign
					print('ERROR: Missing oposing sign for '+str(sign))
					print('Expected a priority_road_left sign on '+str(sign_road.right))
					return False
				elif oposing_sign[0].name!='priority_road_left': # Found other sign
					print('ERROR: Wrong oposing sign for '+str(sign))
					print('Expected a priority_road_left sign on '+str(sign_road.right))
					return False
		elif sign.name=='priority_road_left':
			if sign_road.left == None:
				print('ERROR: A priority_road_left sign is placed on a road with no left connection')
				return False
			else:
				oposing_sign=[s for s in signs if s.road in sign_road.left]
				if oposing_sign==[]: # Found no sign
					print('ERROR: Missing oposing sign for '+str(sign))
					print('Expected a priority_road_right sign on '+str(sign_road.left))
					return False
				elif oposing_sign[0].name!='priority_road_right': # Found other sign
					print('ERROR: Wrong oposing sign for '+str(sign))
					print('Expected a priority_road_right sign on '+str(sign_road.left))
					return False

		# Only 3 roads case is covered by the above checks	
		if nr_roads > 3:
			# We have a stop sign and forward road => it should have the same sign
			if sign.name == 'stop' and sign_road.forward !=None: 
					oposing_sign=[s for s in signs if s.road in sign_road.forward]
					if oposing_sign==[]: # Found no sign
						print('ERROR: Missing oposing sign for '+str(sign))
						print('Expected a stop sign on '+str(sign_road.forward))
						return False
					elif oposing_sign[0].name!='stop': # Found other sign
						print('ERROR: Wrong oposing sign for '+str(sign))
						print('Expected a stop sign on '+str(sign_road.forward))
						return False
			# We have a stop_right sign and right road => it should have the stop_left sign
			elif sign.name == 'stop_right' and sign_road.right !=None: 
					oposing_sign=[s for s in signs if s.road in sign_road.right]
					if oposing_sign==[]:
						print('ERROR: Missing oposing sign for '+str(sign))
						print('Expected a stop_left sign on '+str(sign_road.right))
						return False
					elif oposing_sign[0].name!='stop_left': # Found other sign
						print('ERROR: Wrong oposing sign for '+str(sign))
						print('Expected a stop_left sign on '+str(sign_road.right))
						return False
			# We have a stop_left sign and left road => it should have the stop_right sign
			elif sign.name == 'stop_left' and sign_road.left !=None: 
					oposing_sign=[s for s in signs if s.road in sign_road.left]
					if oposing_sign==[]:
						print('ERROR: Missing oposing sign for '+str(sign))
						print('Expected a stop_right sign on '+str(sign_road.left))
						return False
					elif oposing_sign[0].name!='stop_right': # Found other sign
						print('ERROR: Wrong oposing sign for '+str(sign))
						print('Expected a stop_right sign on '+str(sign_road.left))
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