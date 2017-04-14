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
sns.set_palette("husl")
sns.set(style="whitegrid")

key_types = {'Distribution Type': int,
 'Ant ID': int,
 'Pile ID': int,
 'Y-Position': float,
 'Pickup Time': float,
 'Drop Off Time': float,
 'X-Position': float}
CPFARecordingDir=os.path.join(sys.argv[1],"CPFARecording")
#PlotSaveDir=os.path.join(sys.argv[1],"SavedPlot")
#try:
#    os.makedirs(PlotSaveDir)
#except OSError as exc:  # Python >2.5
#    if exc.errno == errno.EEXIST and os.path.isdir(PlotSaveDir):
#        pass
#    else:
#            raise
averageTimeToOneWayTrip=[]
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
    #data = {}
    for key in key_types:
       #data[key] = []
       for row in reader:
            #data[key].append(key_types[key](row[key]))
            #if (float(row['Drop Off Time'])>0) and (float(row['Pickup Time']>0):
            #    averageTimeToOneWayTrip.append(float(row['Drop Off Time'])- float(row['Pickup Time'])))
            if(float(row['Drop Off Time'])>0 and float(row['Pickup Time'])>0):
                averageTimeToOneWayTrip.append(((float(row['Drop Off Time'])- float(row['Pickup Time']))))
                #print float(row['Drop Off Time'])
    #print averageTimeToOneWayTrip
print sum(averageTimeToOneWayTrip)/len(averageTimeToOneWayTrip)*4
    
