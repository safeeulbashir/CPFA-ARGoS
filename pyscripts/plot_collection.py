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
import Plot_collection_helper
sns.set_palette("husl")
sns.set(style="whitegrid")
##Sample Run
# python pyscripts/plot_collection.py CPFA_saves/2016-08-05_12-32-25 CPFA_saves/2016-08-05_12-32-25/2016-10-11_18-42-14_w60_l5400_s10_c4_p1/ CPFA_saves/2016-08-05_12-32-25/2016-10-11_18-45-18_w60_l5400_s10_c4_p4/ CPFA_saves/2016-08-05_12-32-25/2016-10-11_18-48-24_w60_l5400_s10_c4_p16/

key_types = {'Distribution Type': int,
 'Ant ID': int,
 'Pile ID': int,
 'Y-Position': float,
 'Pickup Time': float,
 'Drop Off Time': float,
 'X-Position': float}
CPFARecordingDir=os.path.join(sys.argv[1],"CPFARecording")
PlotSaveDir=os.path.join(sys.argv[1],"SavedPlot2")
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
    print splitter2[0]
    temporaryPath=os.path.join(CPFARecordingDir,dir)
    with open(temporaryPath, 'r') as csvfile:
        reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
    reader = list(reader)
    data = {}
    for key in key_types:
       data[key] = []
       for row in reader:
            data[key].append(key_types[key](row[key]))

    minutes = range(int(np.max(data['Drop Off Time']) / 60 + 1))
    cumulative_sums = {}

    for i, t in enumerate(data['Drop Off Time']):
        if t != -1:
            t = t / 60
            id = data["Distribution Type"][i]
            if id not in cumulative_sums:
                cumulative_sums[id] = np.zeros(len(minutes))
            for m in minutes:
                if m >= t:
                    cumulative_sums[id][m] += 1
    ChangePointFileName=os.path.join(Plot_collection_helper.AllChangePointSavingDirectory,splitter2[0]+".txt") #Getting the name
    #print dir
    FileToRead=open(ChangePointFileName,'r')
    lines=FileToRead.readlines()
    ChangePointX={}
    ChangePointY={}
    counter=0
    for line in lines:
        PilesAndPoints=line.split()
        for points in PilesAndPoints:
            if points==PilesAndPoints[0]:
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
    #plt.show()
    #pp=PdfPage('multipage.pdf')
    savefigure=os.path.join(PlotSaveDir,'RandomSeed_'+splitter2[0]+'.png')
    plt.savefig(savefigure)
    plt.close()
    #time.sleep(.001)
    #break