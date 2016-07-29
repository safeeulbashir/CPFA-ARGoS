import sys
import numpy as np
import csv
#import os
###############
#example Call##
#######################################################################################################
#python pyscripts/Stats.py CPFA_saves/2016-07-25_13-23-18/2016-07-26_16-57-49_w60_l5400_s10_c4_p1 16 ##
#######################################################################################################

DifferenceInSeconds=list()
pathToCPs="./"+sys.argv[1]+"/ChangePoints.txt"
Directory=str.split(sys.argv[1],"/")
pathToPheromoneRecordingDir="./"+Directory[0]+"/"+Directory[1]+"/"+"PheromoneRecordings/"
cpkey_types = {'RandomSeed': int,
    'CP1': int,
    'CP2': int,
    'CP3': int,
    'CP4': int,
    }
with open(pathToCPs, 'r') as csvfile:
	reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
	reader = list(reader)
	ChangePoints = {}
	for key in cpkey_types:
		ChangePoints[key] = []
		for row in reader:
			ChangePoints[key].append(cpkey_types[key](row[key]))
csvfile.close()
count=0;
for randomseed,cp1,cp2,cp3,cp4 in zip(ChangePoints['RandomSeed'],ChangePoints['CP1'],ChangePoints['CP2'],ChangePoints['CP3'],ChangePoints['CP4']):
	#print str(randomseed)+" "+str(cp1)+" "+str(cp2)+" "+str(cp3)+" "+str(cp4)
	pheromones=list()
	np.array(pheromones)
	DifferenceInSeconds.append([])
	DifferenceInSeconds[count].append(randomseed)
	pathToPheromoneFile=pathToPheromoneRecordingDir+"RandomSeed_"+str(randomseed)+".pheromone"
	print randomseed
	f = open(pathToPheromoneFile,'r')
	for line in f.readlines():
		line=str.split(line," ")
		if(line[1]==sys.argv[2]):		
			#DifferenceInSeconds[count].append(cp1)
			for x in range(2, len(line)):
				print line[x]
				if(line[x]!='\n'):
					pheromones.append(line[x])
	f.close()
	cps=np.array([cp1,cp2,cp3,cp4])
	#print cps
	for cp in cps:	# Adding the values less then each change point in an arrays
		tempPheromones=list() #values those are less then a cp
		for pheromone in pheromones:
			if(int(pheromone)<=int(cp)): #conditional check
				tempPheromones.append(int(pheromone))
		tempPheromones=np.array(tempPheromones)
		tempPheromones=np.sort(tempPheromones)
		#print tempPheromones
		if(len(tempPheromones)>0): #checks if no pheromone laying event is there before the change point.
			diff=cp-tempPheromones[len(tempPheromones)-1]
		else: diff=-1
		#print diff
		DifferenceInSeconds[count].append(diff)
	count=count+1
	#break
print DifferenceInSeconds