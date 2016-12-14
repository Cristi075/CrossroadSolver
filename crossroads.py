import sys
import jsonpickle

from common import *
from generate import generate
from parse import parse
from programs import program0

def help():
	print('Available commands:')
	print('	crossroads print filenname - prints the scenario from the file')
	print('	crossroads solve filename - loads the scenario and solves it')
	print('	crossroads parse inFile outFile - parses the inputFile and writes a scenario file in outFile')
	print('		The format for the inFile can be found in help.txt')
	print('	crossroads generate outFile - interactive scenario generator')
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
		fileName1=arguments[1]
		print('Trying to open '+fileName1)
		inputFile=open(fileName1,'r')
		env=jsonpickle.decode(inputFile.read())
		print("Loaded scenario from "+fileName1)
		print(env)
	elif (command == 'solve'):
		fileName1=arguments[1]
		print('Trying to open '+fileName1)
		inputFile=open(fileName1,'r')
		env=jsonpickle.decode(inputFile.read())
		print('Scenario loaded. Running ... '+fileName1)
		env.run()
	elif (command == 'generate'):
		fileName1=arguments[1]
		print('Trying to open '+fileName1)
		outputFile=open(fileName1,'w')
		env=generate()
		if(env!=None):
			outputFile.write(jsonpickle.encode(env))
			outputFile.close()

	elif (command == 'parse'):
		if(len(arguments)!=3):
			print('Invalid command:'+arguments[0])
			help()

		fileName1=arguments[1]
		fileName2=arguments[2]
		print('Trying to open '+fileName1)
		inputFile=open(fileName1,'r')
		outputFile=open(fileName2,'w')

		parse(inputFile,outputFile)
	else:
		print('Invalid command:'+arguments[0])
		help()
except IOError as err:
	print('IOError:'+err.strerror)