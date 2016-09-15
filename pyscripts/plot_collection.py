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
    plt.figure()
    plt.hold(True)
    color=["red","yellow","green","blue"]
    colorSorter=0
    for id in sorted(cumulative_sums.keys()):
        plt.plot(minutes, cumulative_sums[id], label=str(id), color=color[colorSorter])
        colorSorter=colorSorter+1
    plt.xlabel('time (min)')
    plt.ylabel('seeds collected')
    plt.legend(loc='best')
    #plt.show()
    #pp=PdfPage('multipage.pdf')
    savefigure=os.path.join(PlotSaveDir,'RandomSeed_'+splitter2[0]+'.png')
    plt.savefig(savefigure)
    plt.close()
    #time.sleep(.001)
    #break