import sys
import glob
import os
#import argos_util
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse
import numpy as np
import seaborn as sns
import csv
import errno    
import time
import FieldDataPlotterHelper
sns.set_palette("husl")
sns.set(style="whitegrid")
key_types = {'Dist': int,
 'Ant': int,
 'Pile': float,
 'Y-Position': float,
 'Pickup': float,
 'Drop': float,
 'X-Position': float}
CPFARecordingDir=os.path.join(sys.argv[1],"FoagingRecording")
PlotSaveDir=os.path.join(sys.argv[1],"SavedPlot")
try:
    os.makedirs(PlotSaveDir)
except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(PlotSaveDir):
        pass
    else:
            raise
dirs = os.listdir(CPFARecordingDir)
for dir in dirs:
    splitter= dir.split("_")
    tempSplit=splitter[1]
    splitter2=tempSplit.split(".")
    #print splitter2[0]
    temporaryPath=os.path.join(CPFARecordingDir,dir)
    with open(temporaryPath, 'r') as csvfile:
        reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
    reader = list(reader)
    data = {}
    for key in key_types:
       data[key] = []
       for row in reader:
            data[key].append(key_types[key](row[key]))

    minutes = range(int(np.max(data['Drop']) / 60 + 1))
    cumulative_sums = {}
    for i, t in enumerate(data['Drop']):
        if t != -1:
            t = t / 60
            id = data["Dist"][i]
            if id not in cumulative_sums:
                cumulative_sums[id] = np.zeros(len(minutes))
            for m in minutes:
                if m >= t:
                    cumulative_sums[id][m] += 1
    ChangePointFileName=os.path.join(FieldDataPlotterHelper.AllChangePointSavingDirectory,dir) #Getting the name
    FileToRead=open(ChangePointFileName,'r')
    lines=FileToRead.readlines()
    ChangePointX={}
    ChangePointY={}
    counter=0
    #print ChangePointFileName
    for line in lines:
        PilesAndPoints=line.split()
        #print PilesAndPoints
        for points in PilesAndPoints:
            if points==PilesAndPoints[0]:
                #print  points
                pileId=int(points)
                try:
                    len(cumulative_sums[pileId])
                except:
                    break 
                ChangePointY[pileId]=np.zeros(len(PilesAndPoints)-1)
                ChangePointX[pileId]=np.zeros(len(PilesAndPoints)-1)
                counter=0
                #print "ID is "+str(pileId)
                #print cumulative_sums[pileId]
                #print ChangePointX
            else:
                ChangPointMinute= int(points)/60
                #print "Pile Id:"+str(pileId)+" Point:"+str(ChangPointMinute)
                ChangePointX[pileId][counter]=ChangPointMinute
                ChangePointY[pileId][counter]=cumulative_sums[pileId][ChangPointMinute]
                counter=counter+1 

    FileToRead.close()
    plt.figure()
    plt.hold(True)
    color=["red","purple","green","blue"]
    colorSorter=0
    for id in sorted(cumulative_sums.keys()):
        plt.plot(minutes, cumulative_sums[id], label=str(id), color=color[colorSorter])
        try:
            if id==1:
                plt.plot(ChangePointX[id],ChangePointY[id],'ro')
            elif id==4:
                plt.plot(ChangePointX[id],ChangePointY[id],'b*')
            elif id==16:
                plt.plot(ChangePointX[id],ChangePointY[id],'go')
        except:
            pass
        colorSorter=colorSorter+1
    plt.xlabel('time (min)', fontsize=20)
    plt.ylabel('seeds collected', fontsize=20)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=20) 
    plt.legend(loc='best',prop={'size':12})
    #for i in range(2,5):
     #   pathToCP=sys.argv[i]

        
    #plt.show()
    #pp=PdfPage('multipage.pdf')
    savefigure=os.path.join(PlotSaveDir,dir+'.png')
    plt.savefig(savefigure)
    plt.close()
    #time.sleep(.001)
    #break