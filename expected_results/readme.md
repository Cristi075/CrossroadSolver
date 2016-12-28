# Expected results
This folder should contain txt files that will be used for automatic testing.  
The name of each txt file from this folder should correspond to a json file from the test_scenarios folder (for example scenario1.txt from this folder will be the expected result for running scenario1.json)  
## Format
* If you expect the scenario to end up in a deadlock that will be detected and solved write 'Deadlock' (case-sensitive)
* If you expect the scenario to end up in a deadlock that won't be solved write 'Fail' (case-sensitive)
* Otherwise, write the name of the drivers one on each line, exactly as you wrote them in the txt file that defined the scenario in the order they should go through the crossroad