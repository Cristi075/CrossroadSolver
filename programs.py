
def program0(percepts):
    myself=percepts[0]
    agents=percepts[1]
    roads=percepts[2]
    signs=percepts[3]

    my_road=next(road for road in roads if road.name == myself.current_road)

    emergency_agents=[agent for agent in agents if (agent.emergency and agent.alive)]

    # If my vehicle is an emergency one i should go without waiting
    # TODO: What happens if we have more than one emergency vehicle
    if myself.emergency: 
        return 'go'

    # If there are emergency vehicles present i should wait for them to pass  
    if not myself.emergency and emergency_agents:
        print(myself.name+': I am waiting for the emergency vehicles to pass')
        return 'wait'

    if myself.destination_road in my_road.right: 
        # If i'm taking a right turn then i don't have to wait for anyone
        return 'go'

    for agent in agents:
        # I have to wait for the agents that are on my right side
        if agent.current_road in my_road.right and agent.alive:
            return 'wait'
    
    if myself.destination_road in my_road.left:
        # I'm taking a left turn.
        # Check if the agent on the oposite road is also taking a left turn
        oposing_agents=[agent for agent in agents if agent.current_road in my_road.forward]
        if(oposing_agents!=[]):
            oposing_agent=oposing_agents[0]
            oposing_agents=oposing_agents[1:]
        else:
            # There are no agents on the oposite road
            return 'go'

        # If the other agent is not active we shouldn't wait for them
        if not oposing_agent.alive:
            return 'go'

        if oposing_agent.destination_road in my_road.right:
            # If the other agent wants to get to a road that's on my right
            # It means that he also takes a left turn
            # We can both pass at the same time
            return 'go'
        else:
            # If the other agent isn't taking a left turn too i have to wait for him
            return 'wait'

    return 'go'
