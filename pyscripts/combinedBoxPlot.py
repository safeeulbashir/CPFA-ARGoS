import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import re

PathToAnalysis=sys.argv[1]
pathTositeFidelityRecordingDir=PathToAnalysis+"SiteFidelityRecordings/"
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
		siteFidelitys=list()
		np.array(siteFidelitys)
		FalsePositive.append([])
		TruePositive.append([])
		TruePositive[count].append(randomseed)
		FalsePositive[count].append(randomseed)
		pathTositeFidelityFile="./"+pathTositeFidelityRecordingDir+"RandomSeed_"+str(randomseed)+".siteFidelity"
		#print pathTositeFidelityFile
		f = open(pathTositeFidelityFile,'r')
		for line in f.readlines():
			line=str.split(line," ")
			if(line[1]==PileID):		
				for x in range(2, len(line)):
					#print line[x]
					if(line[x]!='\n'):
						siteFidelitys.append(line[x])
		f.close()
		cps=np.array([cp1,cp2,cp3,cp4])
		for cp in cps:	# Adding the values less then each change point in an arrays
			TotalChangepointCounter=TotalChangepointCounter+1
			tempsiteFidelitys=list() #values those are less then a cp
			tempsiteFidelitys2=list()#Values used for false positive
			for siteFidelity in siteFidelitys:
				if(int(siteFidelity)<=int(cp)): #conditional check
					tempsiteFidelitys.append(int(siteFidelity))
			tempsiteFidelitys=np.array(tempsiteFidelitys)
			tempsiteFidelitys=np.sort(tempsiteFidelitys)
			if(len(tempsiteFidelitys)>0): #checks if no siteFidelity laying event is there before the change point.
				diff=cp-tempsiteFidelitys[len(tempsiteFidelitys)-1]
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
				for siteFidelity in siteFidelitys: # for changepoints that occures before siteFidelity laying event.
					if(int(siteFidelity)>=int(cp)): #conditional check
						tempsiteFidelitys2.append(int(siteFidelity))
				tempsiteFidelitys2=np.array(tempsiteFidelitys2)
				tempsiteFidelitys2=np.sort(tempsiteFidelitys2)
				if(len(tempsiteFidelitys2)>0): # Check if there is any false positive points
					falseP=tempsiteFidelitys2[0]-cp #the smallest value is at 0th Index
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
	print "Change point within 10 seconds of laying siteFidelity "+str(ChangePointInTenSeconds)
	print "Change point within 300 seconds of laying siteFidelity "+str(ChangePointInThreeHSeconds)
	print "Change point within more then 300 seconds of laying siteFidelity "+str(ChangePointHigh)
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
plotter=plt.boxplot(totalTrueSelector,0,"")
plt.xticks([1, 2, 3], ['One Pile', 'Four Pile', 'Sixteen Pile'], size=30)
plt.ylabel('Difference between Site Fidelity Followed and Changepoint Detection',{'fontsize': 15})
plt.title('Site Fidelity Only Parameter and Constant Detrended Cumulative Sum method',{'fontsize': 20})
plt.show() 
