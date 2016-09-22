import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import re
#For Constant Detrending
#python pyscripts/combinedBoxPlotpheromone.py CPFA_saves/2016-08-05_12-32-25/ CPFA_saves/2016-08-05_12-32-25/2016-08-08_18-49-13_w60_l5400_s10_c4_p1 CPFA_saves/2016-08-05_12-32-25/2016-08-09_13-05-52_w60_l5400_s10_c4_p4 CPFA_saves/2016-08-05_12-32-25/2016-08-09_13-22-03_w60_l5400_s10_c4_p16
#For Linear Detrending 
#python pyscripts/combinedBoxPlotpheromone.py CPFA_saves/2016-08-05_12-32-25/ CPFA_saves/2016-08-05_12-32-25/2016-08-08_19-01-14_w60_l5400_s10_c4_p1 CPFA_saves/2016-08-05_12-32-25/2016-09-21_18-05-25_w60_l5400_s10_c4_p4 CPFA_saves/2016-08-05_12-32-25/2016-08-09_13-11-38_w60_l5400_s10_c4_p16

PathToAnalysis=sys.argv[1]
pathToPheromoneRecordingDir=PathToAnalysis+"PheromoneRecordings/"
#print pathTositeFidelityRecordingDir
#print range(1:3)
totalTrueSelector=[]
plotcounter=0
for i in range(2,len(sys.argv)):
	totalTrueSelector.append([])
	#print sys.argv[i]
	#totalTrueSelector[plotcounter]=list()
	ChangePointInTenSeconds=0 # Change point within 10 seconds of siteFidelity laying event
	ChangePointInThreeHSeconds=0 # Change point within 300 hundred seconds siteFidelity laying event
	TotalChangepointCounter=0
	TruePositiveCounter=0
	FalsePositiveCounter=0
	ChangePointHigh=0 #Change points which has diff greter then 300 seconds
	TruePositivePoints=list()
	TruePositive=list()
	FalsePositive=list()
	pathToCPs="./"+sys.argv[i]+"/ChangePoints.txt"
	pileSplitter=str.split(sys.argv[i],"_") #Extracts the pile number
	print pileSplitter
	PileID=re.sub('[p/]', '', pileSplitter[8])
	print PileID
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
	count=0
	for randomseed,cp1,cp2,cp3,cp4 in zip(ChangePoints['RandomSeed'],ChangePoints['CP1'],ChangePoints['CP2'],ChangePoints['CP3'],ChangePoints['CP4']):
		pheromones=list()
		np.array(pheromones)
		FalsePositive.append([])
		TruePositive.append([])
		TruePositive[count].append(randomseed)
		FalsePositive[count].append(randomseed)
		pathToPheromoneFile="./"+pathToPheromoneRecordingDir+"RandomSeed_"+str(randomseed)+".pheromone"
		#print pathTositeFidelityFile
		f = open(pathToPheromoneFile,'r')
		for line in f.readlines():
			line=str.split(line," ")
			if(line[1]==PileID):		
				for x in range(2, len(line)):
					#print line[x]
					if(line[x]!='\n'):
						pheromones.append(line[x])
		f.close()
		cps=np.array([cp1,cp2,cp3,cp4])
		for cp in cps:	# Adding the values less then each change point in an arrays
			TotalChangepointCounter=TotalChangepointCounter+1
			temppheromones=list() #values those are less then a cp
			temppheromones2=list()#Values used for false positive
			for pheromone in pheromones:
				if(int(pheromone)<=int(cp)): #conditional check
					temppheromones.append(int(pheromone))
			temppheromones=np.array(temppheromones)
			temppheromones=np.sort(temppheromones)
			if(len(temppheromones)>0): #checks if no siteFidelity laying event is there before the change point.
				diff=cp-temppheromones[len(temppheromones)-1]
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
				for pheromone in pheromones: # for changepoints that occures before siteFidelity laying event.
					if(int(pheromone)>=int(cp)): #conditional check
						temppheromones2.append(int(pheromone))
				tempsitepheromone2=np.array(temppheromones2)
				temppheromones2=np.sort(temppheromones2)
				if(len(temppheromones2)>0): # Check if there is any false positive points
					falseP=temppheromones2[0]-cp #the smallest value is at 0th Index
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
	totalTrueSelector[plotcounter].append(TruePositivePoints)
	#ax1[plotcounter].boxplot(TruePositivePoints)
	#ax1[plotcounter].set_title('Default', fontsize=10)

	#plotter=plt.boxplot(TruePositivePoints,0,"")
	#plotter=plt.boxplot(TruePositivePoints)
	#plt.setp(plotter['boxes'], color='black')
	#plt.setp(plotter['whiskers'], color='black')
	#plt.setp(plotter['fliers'], color='red', marker='+')
	#plt.set_axisbelow(True)
	#ax1.set_title('Bla')
	#ax1.set_xlabel('Distribution')
	#ax1.set_ylabel('Bla')
	#for item in plotter['fliers']:
	#	print item.get_ydata()
	#plt.show()
	#figure, ax2= plt.subplots(figsize=(10, 6))
	plotcounter=plotcounter+1
#for ax in ax1.flatten():
#	ax.set_yscale('log')
#boxprops = dict(linestyle='--', linewidth=3, color='darkgoldenrod')
plotter=plt.boxplot(totalTrueSelector,patch_artist=True)
#print plotter
#plt.ylim(0,2000)
#plt.xlim(0,1)
plt.boxwex=10
plt.setp(plotter['boxes'],color='black',facecolor="darkkhaki",lw=7)
plt.setp(plotter['whiskers'],color='black',lw=5)
plt.setp(plotter['medians'],color="red",lw=5)
plt.setp(plotter['caps'],lw=5)
plt.xticks([1, 2, 3], ['One Pile', 'Four Pile', 'Sixteen Pile'], size=45)
plt.yticks(size=40)
plt.ylabel('Time Difference',{'fontsize': 45})
plt.title('Cumulative Sum method',{'fontsize': 50})
plt.show() 
