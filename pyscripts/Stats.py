import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
#import os
###############
#example Call##
#######################################################################################################
#python pyscripts/Stats.py CPFA_saves/2016-07-25_13-23-18/2016-07-26_16-57-49_w60_l5400_s10_c4_p1 16 ##
#######################################################################################################
ChangePointInTenSeconds=0 # Change point within 10 seconds of pheromone laying event
ChangePointInThreeHSeconds=0 # Change point within 300 hundred seconds pheromone laying event
TotalChangepointCounter=0
TruePositiveCounter=0
FalsePositiveCounter=0
ChangePointHigh=0 #Change points which has diff greter then 300 seconds
TruePositivePoints=list()
TruePositive=list()
FalsePositive=list()
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
	pheromones=list()
	np.array(pheromones)
	FalsePositive.append([])
	TruePositive.append([])
	TruePositive[count].append(randomseed)
	FalsePositive[count].append(randomseed)
	pathToPheromoneFile=pathToPheromoneRecordingDir+"RandomSeed_"+str(randomseed)+".pheromone"
	f = open(pathToPheromoneFile,'r')
	for line in f.readlines():
		line=str.split(line," ")
		if(line[1]==sys.argv[2]):		
			for x in range(2, len(line)):
				#print line[x]
				if(line[x]!='\n'):
					pheromones.append(line[x])
	f.close()
	cps=np.array([cp1,cp2,cp3,cp4])
	for cp in cps:	# Adding the values less then each change point in an arrays
		TotalChangepointCounter=TotalChangepointCounter+1
		tempPheromones=list() #values those are less then a cp
		tempPheromones2=list()#Values used for false positive
		for pheromone in pheromones:
			if(int(pheromone)<=int(cp)): #conditional check
				tempPheromones.append(int(pheromone))
		tempPheromones=np.array(tempPheromones)
		tempPheromones=np.sort(tempPheromones)
		if(len(tempPheromones)>0): #checks if no pheromone laying event is there before the change point.
			diff=cp-tempPheromones[len(tempPheromones)-1]
			TruePositivePoints.append(diff)
			falseP=-1
			TruePositiveCounter=TruePositiveCounter+1
			if(0<=diff<=10):
				ChangePointInTenSeconds=ChangePointInTenSeconds+1
			elif(11<=diff<=300):
				ChangePointInThreeHSeconds=ChangePointInThreeHSeconds+1
			else: ChangePointHigh=ChangePointHigh+1
		else: 
			diff=-1
			for pheromone in pheromones: # for changepoints that occures before pheromone laying event.
				if(int(pheromone)>=int(cp)): #conditional check
					tempPheromones2.append(int(pheromone))
			tempPheromones2=np.array(tempPheromones2)
			tempPheromones2=np.sort(tempPheromones2)
			if(len(tempPheromones2)>0): # Check if there is any false positive points
				falseP=tempPheromones2[0]-cp #the smallest value is at 0th Index
				FalsePositiveCounter=FalsePositiveCounter+1
			else: falseP=-1
		FalsePositive[count].append(falseP)
		TruePositive[count].append(diff)
	#print randomseed
	#print TruePositive[count]
	count=count+1
#print TruePositive
#print FalsePositive
print "Total Change Points "+ str(TotalChangepointCounter)
print "True Positive Counter "+str(TruePositiveCounter)
print "False Positive Counter "+str(FalsePositiveCounter)
print "Change point within 10 seconds of laying pheromone "+str(ChangePointInTenSeconds)
print "Change point within 300 seconds of laying pheromone "+str(ChangePointInThreeHSeconds)
print "Change point within more then 300 seconds of laying pheromone "+str(ChangePointHigh)
fig, ax1 = plt.subplots(figsize=(10, 6))
plotter=plt.boxplot(TruePositivePoints,0,"")
#plotter=plt.boxplot(TruePositivePoints)
plt.setp(plotter['boxes'], color='black')
plt.setp(plotter['whiskers'], color='black')
plt.setp(plotter['fliers'], color='red', marker='+')
#plt.set_axisbelow(True)
ax1.set_title('Time between pheromone laying event followed by change point detection event for '+ sys.argv[3]+' detrended cumulative sum')
#ax1.set_xlabel('Distribution')
ax1.set_ylabel('Difference in Second')
#for item in plotter['fliers']:
#	print item.get_ydata()
#plt.show()
figure, ax2= plt.subplots(figsize=(10, 6))
#ax = axes([0.1, 0.1, 0.8, 0.8])

fracs = [1.0*ChangePointInTenSeconds/TruePositiveCounter,\
		1.0*ChangePointInThreeHSeconds/TotalChangepointCounter,\
		1.0*ChangePointHigh/TotalChangepointCounter,1.0*FalsePositiveCounter/TotalChangepointCounter]
summa=1.0*ChangePointInTenSeconds/TotalChangepointCounter+\
		1.0*ChangePointInThreeHSeconds/TotalChangepointCounter+\
		1.0*FalsePositiveCounter/TotalChangepointCounter
print summa
explode=(0, 0.05, 0, 0)
labels="Change Point Detected within 10 seconds of Laying Pherommone",\
		"Change Point Detected within 300 seconds of laying pheromone",\
		"Pheromone Followed but change point detected after 300 seconds",\
		"Pheromone Followed but no change point detected"
piebaba=plt.pie(fracs,autopct='%1.1f%%', shadow=True, startangle=90)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

fontP = FontProperties()
fontP.set_size('small')
#pylab.legend(prop = fontP, ....)
plt.legend(labels,"lower left",prop=fontP)
plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
ax2.set_title('Accuracy of the model with '+sys.argv[3]+' detrended cumulative sum')
#top_points = plotter["fliers"][0].get_data()[1]
#bottom_points = plotter["fliers"][2].get_data()[1]
#print plotter["fliers"][1].get_data()[1]
#plt.plot(np.ones(len(top_points)), top_points, "+")
plt.show() 