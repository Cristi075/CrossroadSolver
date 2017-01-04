# Script used for automated testing
import os
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

devNull = open(os.devnull, 'w')
count=1
correct=0
deadlock=0

labels=['Correct','Wrong','Deadlock']
colors=['Green','Red','Magenta']

for file in os.listdir('test_scenarios'):
	if file.endswith('.json'):
		inFile='test_scenarios/'+file
		subprocess.call(['python3','crossroads.py','solve',inFile],stdout=devNull)

		try:
			resultFile=open('result.txt','r')
		except:
			print('Could not open result.txt')
			exit()

		result=resultFile.read()
		filename,extension=os.path.splitext(file)

		try:
			expectedName='expected_results/'+filename+'.txt'
			expectedFile=open(expectedName,'r')
		except:
			print('Could not open file containing expected result ('+filename +' .txt )')
			exit()

		expected=expectedFile.read()

		print('Test nr.'+str(count)+' : '+file+'  ',end='')
		count+=1
		# Testing if the file match after the newlines and spaces are removed
		if(result.strip('\n ') == expected.strip('\n ')): 
			print('MATCH')
			if(result.strip('\n ') == 'Deadlock'):
				deadlock+=1
			else:
				correct+=1
		else:
			print('NO MATCH')
			print('Expected:')
			print(expected.strip('\n '))
			print('But got:')
			print(result.strip('\n '))

print('Finished running tests.')
print(str(count-1)+' tests were ran')
print(str(correct)+' tests were sucesfull')
print(str(deadlock) + ' deadlocks were present in the scenarios and they were properly detected')
print(str(count-1-correct-deadlock)+' tests failed')

sizes=[correct,count-1-correct-deadlock,deadlock]
plt.pie(sizes,labels=labels,colors=colors)
plt.savefig('plot.png')