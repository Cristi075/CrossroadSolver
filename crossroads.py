import sys
import jsonpickle

from common import *
from parse import parse
from programs import program0

def help():
	print('Available commands:')
	print('	crossroads print filenname - prints the scenario from the file')
	print('	crossroads solve filename - loads the scenario and solves it')
	print('	crossroads parse inFile outFile - parses the inputFile and writes a scenario file in outFile')
	print('		The format for the inFile can be found in help.txt')
	print('	crossroads help - displays this message')
	exit()

arguments=sys.argv[1:]

# TODO: Replace this with an argparser
# No argument
if(len(arguments)<1):
	print('Invalid command')
	help()

# A single argument
if(len(arguments)==1):
	if(arguments[0] == 'help'):
		help()
	else:
		print('Invalid command')
		help()

command=arguments[0]

try:
	if(command == 'print'):
		try:
			fileName1=arguments[1]
			print('Trying to open '+fileName1)
			inputFile=open(fileName1,'r')
		except:
			print('Could not open file'+fileName1)
			exit()

		env=jsonpickle.decode(inputFile.read())
		print("Loaded scenario from "+fileName1)
		print(env)
	elif (command == 'solve'):
		try:
			fileName1=arguments[1]
			print('Trying to open '+fileName1)
			inputFile=open(fileName1,'r')
		except:
			print('Could not open file'+fileName1)
			exit()

		env=jsonpickle.decode(inputFile.read())
		print('Scenario loaded. Running ... '+fileName1)

		env.run()
		
		# Creating a file where the order will be written. This file might be useful for automated testing
		try:
			resultFile=open('result.txt','w')
		except:
			print('Could not create result.txt')
			exit()

		print('Simulation ended')
		print('Order:')
		print(env.order)
		if(env.deadlock):
			# If a deadlock occurs i will simply write deadlock since the result is not deterministic in most deadlock cases
			resultFile.write('Deadlock\n') 
			print('A deadlock occured')
		else:
			for name in env.order:
				resultFile.write(name)
				resultFile.write('\n')
		resultFile.close()

	elif (command == 'parse'):
		if(len(arguments)!=3):
			print('Invalid command:'+arguments[0])
			help()

		try:
			fileName1=arguments[1]
			print('Trying to open '+fileName1)
			inputFile=open(fileName1,'r')
		except:
			print('Could not open file'+fileName1)
			exit()

		try:
			fileName2=arguments[2]
			print('Trying to open '+fileName2)
			outputFile=open(fileName2,'w')
		except:
			print('Could not open file'+fileName2)
			exit()

		parse(inputFile,outputFile)
	else:
		print('Invalid command:'+arguments[0])
		help()
except IOError as err:
	print('IOError:'+err.strerror)