#!/bin/bash

# A small bash script that i use to parse every .txt file in the test_scenarios folder
for inFile in $( ls test_scenarios | grep -e ".txt")
do
	fileName=$(echo "$inFile" | cut -d '.' -f 1)
	fileExt=$(echo "$inFile" | cut -d '.' -f 2)
	if [ $fileExt=='.txt' ]; then # In case something else gets here don't do anything
		outFile=$fileName.json
		echo $inFile -\> $outFile
		python3 crossroads.py parse test_scenarios/$inFile test_scenarios/$outFile
	fi
done
