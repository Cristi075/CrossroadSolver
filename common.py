from aima.agents import *

class Crossroad(Environment):
    def __str__(self):
        result='Roads:\n'
        roads=[thing for thing in self.things if isinstance(thing,Road)]
        for road in roads:
            result= result + str(road)+'\n'
        result=result + '\nAgents:'
        agents=[thing for thing in self.things if isinstance(thing,Agent)]
        for agent in agents:
            result= result + str(agent) + '\n'
        signs=[thing for thing in self.things if isinstance(thing,Sign)]
        result=result + '\nSigns:'
        for sign in signs:
            result= result + str(sign) + '\n'
        return result

    # Returns the road the road with the given name if it exists
    def getRoadByName(self,name):
        roads=[thing for thing in self.things if isinstance(thing,Road)]
        for road in roads:
            if road.name is name:
                return road
        return None

    # An agent will receive a list with differnet elements from the environment
    # The first element will be the agent itself
    # The second element will be a list containing other agents
    # The third element will be a list containing all the existing roads
    # The fourth element will be a list containing all the signs that exist on the same road as the agent
    def percept(self,agent):
        other_agents=[thing for thing in self.things if (isinstance(thing,Agent) and thing!= agent)]
        roads=[thing for thing in self.things if isinstance(thing,Road)]
        signs=[thing for thing in self.things if isinstance(thing,Sign) and thing.road==agent.current_road]
        return agent,other_agents,roads,signs

    # If an agent takes the 'go' action it will become inactive
    def execute_action(self,agent,action):
        if action is 'go':
            print (agent.name + ' went from ' + agent.current_road + ' to ' + agent.destination_road)
            agent.alive=False
        elif action is 'wait':
            print (agent.name + ' is waiting')
        elif action is '': # NOOP
            pass
        else: # The action was not defined
            print('ERROR: Illegal action '+action)

class Driver(Agent):
    def __init__(self,program,name,current_road,destination_road,emergency=False):
        super().__init__(program)
        self.alive=True
        self.name=name
        self.current_road=current_road
        self.destination_road=destination_road
        self.emergency=emergency

    def __str__(self):
        result='Name: '+self.name + '\n'
        result=result + 'Current road: '+self.current_road + '\n'
        result=result + 'Destination road:'+self.destination_road + '\n'
        result=result + 'Active:'+ str(self.alive) + '\n'
        if self.emergency:
            result=result+'Emergency vehicle'
        return result

class Road(Thing):
    def __init__(self,name,left,forward,right):
        self.name=name
        self.left=left
        self.forward=forward
        self.right=right

    def __str__(self):
        result='Road name:'+self.name+'\n'
        result= result + 'Left side:'+str(self.left)+'\n'
        result= result + 'Forward:'+str(self.forward)+'\n'
        result= result + 'Right side:'+str(self.right)+'\n'
        return result

# The class that i will use to represent a traffic sign
# A sign can have the following names:
# priority_road, priority_road_left, priority_road_right 
# In this case left/right is the direction where the priority road is going
# stop, stop_left, stop_right
# The yield sign can be considered the same as the stop one since it has the same effect in our situation
# In this case left/right is the dirrection of the other road that has a similar sign(yield or stop)
class Sign(Thing):
    def __init__(self,name,road):
        self.name=name
        self.road=road

    def __str__(self):
        return self.name+ ' on '+ self.road
