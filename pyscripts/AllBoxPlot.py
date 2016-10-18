#Ref: http://matplotlib.org/examples/pylab_examples/boxplot_demo2.html
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import re
from matplotlib.patches import Polygon
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

fig, ax1 = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('A Boxplot Example')
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
bp = plt.boxplot(totalTrueSelector,notch=0, sym='+', vert=1, whis=1.5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')
# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
# Hide these grid behind plot objects
ax1.set_axisbelow(True)
ax1.set_title('Comparison of efficiency of Four Different method for Changepoint Detection')
#ax1.set_xlabel('Distribution')
ax1.set_ylabel('Seconds(s)')
# Now fill the boxes with desired colors
boxColors = ['darkkhaki', 'royalblue', 'green']
numBoxes = 6
medians = list(range(numBoxes))
for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = list(zip(boxX, boxY))
    # Alternate between Dark Khaki and Royal Blue
    k = i % 3
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
    ax1.add_patch(boxPolygon)
    # Now draw the median lines back over what we just filled in
    med = bp['medians'][i]
    medianX = []
    medianY = []
    for j in range(2):
        medianX.append(med.get_xdata()[j])
        medianY.append(med.get_ydata()[j])
        plt.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]
    # Finally, overplot the sample averages, with horizontal alignment
    # in the center of each box
    plt.plot([np.average(med.get_xdata())], [np.average(totalTrueSelector[i])],
             color='w', marker='*', markeredgecolor='k')
    # Set the axes ranges and axes labels
ax1.set_xlim(0.5, numBoxes + 0.5)
top = 4000
bottom = -100
ax1.set_ylim(bottom, top)
#xlabel=['One Pile', 'Four Pile', 'Sixteen Pile']
#xtickNames = plt.setp(ax1, xticklabels=np.tile(xlabel, 4))
#plt.setp(xtickNames, rotation=90, fontsize=20)
# Due to the Y-axis scale being different across samples, it can be
# hard to compare differences in medians across the samples. Add upper
# X-axis tick labels with the sample medians to aid in comparison
# (just use two decimal places of precision)
print medians
pos = np.arange(numBoxes) + 1
upperLabels = [str(np.round(s, 2)) for s in medians]
weights = ['bold', 'semibold','semibold']
for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
    k = tick % 3
    ax1.text(pos[tick], top - (top*0.05), upperLabels[tick],
             horizontalalignment='center', size=20, weight=weights[k],
             color=boxColors[k])
# Finally, add a basic legend
plt.figtext(0.80, 0.08, ' One Pile',
            backgroundcolor=boxColors[0], color='black', weight='roman',
            size=20)
plt.figtext(0.9, 0.08, 'Four Pile',
            backgroundcolor=boxColors[1],
            color='white', weight='roman', size=20)
plt.figtext(0.80, 0.045, 'Sixteen Pile',
            backgroundcolor=boxColors[2],
            color='white', weight='roman', size=20)
plt.figtext(0.890, 0.045, '*', color='white', backgroundcolor='silver',
            weight='roman', size=20)
plt.figtext(0.895, 0.045, ' Average Value', color='black', weight='roman',
            size=20)
#Adding Category
plt.figtext(0.27, 0.20, 'Linear Detrending', color='black', weight='roman',
            size=20)
#Original One
#plt.figtext(0.33, 0.20, 'Constant Detrending', color='black', weight='roman',
#            size=20)
#For SitefidelityGraph
plt.figtext(0.70, 0.18, 'Constant Detrending', color='black', weight='roman',
            size=20)
#plt.figtext(0.55, 0.18, 'Linear Detrending with\n    Difference in Rate', color='black', weight='roman',
#            size=20)
#plt.figtext(0.75, 0.18, 'Constant Detrending with\n  Difference in Rate', color='black', weight='roman',
#            size=20)

plt.show()
