# Test scenarios

This folder contains txt files that describe scenarios. The txt files can be turned into json files by using the parse command (and json files can be used as input files for the solve command). The jpg/jpeg/png files are not important for the program and they are here only to help the users see the scenario described in the txt file.  
  
## Format
The syntax for writing your own scenarios will be explained in this section.
### Describing roads
A road has an unique name and three lists of roads it is connected to (one for each direction: left, forward and right).
Since for this project we are dealing only with T-shaped and cross-shaped crossroads it is safe to assume that for each dirrection there is either a single road connected or nothing. 
To describe a road you should use the following syntax:
```
    Road(name,left_name,forward_name,right_name)
```
name should be a unique to each road
left\_name, forward\_name  and right\_name should be names of other roads.  
If a road doesn't have a certain connection you should put a whitespace instead of a name.
If you use an invalid name and use the parse command you should receive an error.
**Examples:**
```
    Road(R1,R2,R3,R4)
    Road(R2,R3,R4,R1)
    Road(R3,R4,R1,R2)
    Road(R4,R1,R2,R3)
```
```
    Road(R1,R2,R3,)
    Road(R2,R3,,R1)
    Road(R3,,R1,R2)
```

### Describing drivers
A driver has the following properties that define it:
* name = the name this driver is known by. It should be unique
* current_road = the road where this driver is at the beginning of the simulation
* destination_road = the road where this driver wants to go.
* emergency = If it is true this will be considered an emergency vehicle
* yieldChance = chance of this driver to yield (let other pass) in case of a deadlock. 0 means the driver never yields, 1 means the driver always yields

You have two ways of defining a driver. The first one is defining one without specifying a yieldChance. In this case the default yieldChance (0.8) will be used.
```
    Driver(name,current_road,destination_road,emergency)
```
The second method involves manually specifying the yieldChance
```
    Driver(name,current_road,destination_road,emergency,yieldChance)
```
Another limitation of this project is that you cannot place more than one driver on the same starting road (however, same destination road for multiple drivers is an allowed case).
**Examples**
```
    Driver(Green Car,R1,R3,false)
    Driver(Red Bike,R2,R3,false)
    Driver(Red Car,R3,R1,false)
```
```
    Driver(Driver1,R1,R3,false,1)
    Driver(Driver2,R2,R4,false,1)
    Driver(Driver3,R3,R1,false)
    Driver(Driver4,R4,R2,false,0.5)
```

## Describing signs
A sign has only two properties: a name and the name of road they are placed on.
The only defined signs are the following:
* priority\_road = the road this sign is on is a priority road and the road that is connected to this road on the forward connection is also a priority road
* priority\_right = the road this sign is on is a priority road and the road that is connected to this road on the right connection is also a priority road
* priority\_left = the road this sign is on is a priority road and the road that is connected to this road on the left connection is also a priority road
* stop = the drivers on the road this sign is on should wait for the drivers that are on the left road and on the right road
* stop\_right = the drivers on the road this sign is on should wait for the drivers that are on the left road and the one in front of their current road (forward)
* stop\_left = the drivers on the road this sign is on should wait for the drivers that are on the right road and the one in front of their current road (forward)

**Examples**
```
    Sign(priority_road_left,R1)
    Sign(priority_road_right,R2)
    Sign(stop_left,R3)
    Sign(stop_right,R4)
```