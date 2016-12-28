# Crossroad Scenario Solver  
This is a project that I implemented for the Introduction to Artificial Intelligence class that i take at the Technical University of Cluj-Napoca.  
The purpose of this project is to take a situation that describes a given number of drivers at a cross-shaped or T-shaped crossroad and determine in which order they will cross according to the rules of the road from Romania.  
For this project I used [aima-python](https://github.com/aimacode/aima-python) and made some small adjustments to it.  
From aima-python I used the environment class to model the crossroad and the agent class to model the drivers and their behaviour.  

## Installation

This project was created and tested using Python3 (3.4.3) running on Fedora 20 and Fedora 23.
To run this project you should follow these steps:
```
* Install git by running 'sudo yum install git'
* Install pip for python3 by running 'sudo yum install python3-pip'
* Run 'sudo python3 -m pip install -U pip'
* Install jsonpickle by running 'sudo pip3 install jsonpickle'
* Clone this git repository
( by running 'git clone https://github.com/Cristi075/CrossroadSolver.git' )
* Go into the newly created folder by using 'cd CrossroadSolver'
* Clone the aima-python repository in the aima folder
( by running 'git clone https://github.com/aimacode/aima-python aima' )
* Copy all the files from the modified folder into the aima folder
( by running 'cp modified/* aima/.' )
```
Now you should be able to use the parse command on scenarios described in .txt files (that follow the format described in test_scenarios folder's readme) and use the solve command on the resulted json files to get the result.
If you want to run automated tests you can use the parse\_all.sh bash script to parse every \.txt file from the test\_scenaros folder and then you can populate the expected\_results folder with files that follow the described format and run runtest\.py to solve all the json files found in the test\_scenarios folder and compare the result with the one that you wrote in the file with a matching name in the expected\_results folder.