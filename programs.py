from common import valid_signs
import random

def getDecision(myself):
    if(random.uniform(0, 1) < myself.yieldChance):
        print(myself.name+": yield")
        return 'yield'
    else:
        print(myself.name+": try")
        return 'try'

def program0(percepts):
    myself      =percepts[0]
    agents      =percepts[1]
    roads       =percepts[2]
    signs       =percepts[3]
    messages    =percepts[4]


    my_road=next(road for road in roads if road.name == myself.current_road)
    my_signs=[sign for sign in signs if sign.road==my_road.name]

    emergency_agents=[agent for agent in agents if (agent.emergency and agent.alive)]

    nr_active_agents= len([agent for agent in agents if agent.alive])+1
    if(myself.memory['active_agents'] == nr_active_agents):
        # Deadlock situation detected. It the agents is in this case it should start negotiating with the other agents
        #print(messages)
        if(messages=={}):
            # This is the first turn after the deadlock was detected
            return getDecision(myself)            
        else:
            other_messages=[messages[agent.name] for agent in agents if agent.name in messages.keys()]
            if(myself.name in messages.keys()): # This agent sent a message last turn
                if(messages[myself.name]=='yield'):
                    if 'try' not in other_messages: # No agent sent a try message. We're trying again
                        return getDecision(myself)
                    else:
                        return 'yield'
                elif(messages[myself.name]=='try'):
                    if 'try' not in other_messages: # No other agent sent a try message. 
                        return 'go' # This agent is the only one who sent a try message
                    else:
                        return getDecision(myself)

    myself.memory['active_agents'] = nr_active_agents

    # If there are emergency vehicles present i should wait for them to pass  
    if not myself.emergency and emergency_agents:
        print(myself.name+': I am waiting for the emergency vehicles to pass')
        return 'wait'

    if my_signs!=[]:
        sign = my_signs[0]
    else:
        sign = None

    waitFor=[]
    if sign==None: # No signs on the road this agent is on
        # If there are no signs on this road the agent checks if there are stop signs on the left AND right roads
        # If there are stop signs then we should treat this as as an implicit version of the priority_road sign
        signs_right = [ sign for sign in signs if sign.road in my_road.left and sign.name in valid_signs]
        signs_left = [ sign for sign in signs if sign.road in my_road.right and sign.name in valid_signs]
        if signs_left!=[] and signs_left[0].name=='stop' and signs_right!=[] and signs_right[0].name=='stop':
            # Same case as the 'priority_road' case. Look below for that
            if myself.destination_road in my_road.left:
                oposing_agents=[agent for agent in agents if agent.current_road in my_road.forward and agent.alive]
                if oposing_agents!=[]:
                    if oposing_agents[0].destination_road not in my_road.right:
                        waitFor=[oposing_agents[0]]
        else:
            if myself.destination_road in my_road.right: 
                # If i'm taking a right turn then i don't have to wait for anyone
                return 'go'
            
            # Otherwise I have to wait for the agents that are on my right side
            waitFor = [ a for a in agents if a.current_road in my_road.right]

            # If i am making a left turn i have to wait for the agents from the oposite road too
            # Exception: If they are making a left turn too    
            if myself.destination_road in my_road.left:
                oposing_agents=[agent for agent in agents if agent.current_road in my_road.forward and agent.alive]
                if oposing_agents!=[]:
                    if oposing_agents[0].destination_road not in my_road.right:
                        waitFor.append(oposing_agents[0])
    elif sign.name=='stop':
        if len(roads)==3: # I have a stop sign and i'm at a T-shaped crossroad => I have to wait for all the other agents
            waitFor = [ a for a in agents]            
        else:
            # I have to wait for the agents on my left and right
            waitFor = [ a for a in agents if a.current_road in my_road.left or a.current_road in my_road.right]
            # If i am making a left turn i have to wait for the agents from the oposite road too
            # Exception: If they are making a left turn too
            if myself.destination_road in my_road.left:
                oposing_agents=[agent for agent in agents if agent.current_road in my_road.forward and agent.alive]
                if oposing_agents!=[]:
                    if oposing_agents[0].destination_road not in my_road.right:
                        waitFor.append(oposing_agents[0])
    elif sign.name=='stop_left': 
        # I have to wait for the agents on the oposite road and the ones on my right (they have a priority sign)
        # The ones on my left have a stop sign too and they have to give me right-of-way
        waitFor = [ a for a in agents if a.current_road in my_road.forward or a.current_road in my_road.right]
    elif sign.name=='stop_right': # I have to wait for everyone
        waitFor = waitFor = [ a for a in agents] 
    elif sign.name=='priority_road':
        # In case i am making a left turn i should wait for the agent on the oposite road
        # Exception: If they are making a left turn too
        # Otherwise, i should not wait for anyone
        if myself.destination_road in my_road.left:
            oposing_agents=[agent for agent in agents if agent.current_road in my_road.forward and agent.alive]
            if oposing_agents!=[]:
                if oposing_agents[0].destination_road not in my_road.right:
                    waitFor=[oposing_agents[0]]
    elif sign.name=='priority_road_right': # I should wait for the agents on my right
        waitFor = [ a for a in agents if a.current_road in my_road.right]
    elif sign.name=='priority_road_left': # I don't have to wait for anyone
        return 'go'

    # If my vehicle is an emergency one i should wait only for other emergency vehicles
    if myself.emergency: 
        waitFor=[agent for agent in waitFor if agent.emergency]

    for agent in waitFor:
            if agent.alive:
                return 'wait'

    return 'go'
