# Modified files

These are the files from the aima-python repository that I modified.  
Here I will explain what are the changes that I made and the reasons I had for making them.  
You should copy these files (and accept overwriting) after you cloned the aima-python repository to run this project.

## agents.py

```
'from grid import distance2' was changed to 'from .grid import distance2'
```  
I did this because I wanted to be able to import this file from a different folder and I had to make sure that when importing distance2 from grid it will always try to import it from the same dirrectory as the agents.py file.  
  
```
'print('Step' + str(step))'
```  
This line was added to the step method of the Environment class. I wanted to be able to see each step of the simulation separately.  

## grid.py

```
'from utils import clip' was changed to 'from .utils import clip'
```  
I edited this for the same reason as in the agents.py file, I wanted to be able to import this (or the agents.py module to be able to import this) even when I am trying to import it from a different folder.