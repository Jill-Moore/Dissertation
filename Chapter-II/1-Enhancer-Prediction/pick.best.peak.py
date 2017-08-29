#Jill E. Moore
#Weng Lab
#UMass Medical School
#Updated March 2016

import sys

rankcolumn=int(sys.argv[2])-1
intersections=open(sys.argv[1])

vistaDict={}
for line in intersections:
    x=line.rstrip().split("\t")
    element=x[0]+x[1]+x[2]
    try:
    	if element not in vistaDict:
        	vistaDict[element]=[float(x[rankcolumn]), line.rstrip()]
    	else:
        	if vistaDict[element][0] < float(x[rankcolumn]):
            		vistaDict[element]=[float(x[rankcolumn]), line.rstrip()]
    except:
	pass    
            
for element in vistaDict:
    print vistaDict[element][1]

intersections.close()
