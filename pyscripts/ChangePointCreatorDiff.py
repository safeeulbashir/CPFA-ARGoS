import sys
import glob
import os
import re
import datetime
import matplotlib.pyplot as plt
import numpy as np
import argparse
import csv
import scipy.signal
import errno
import subprocess
import signal
# Example Call
# python pyscripts/ChangePointCreatorDiff.py -w 60 -m 10 -l 5400 -d 1 -c 4 -detrending 1 CPFA_saves/2016-06-28_18-37-00
# -w =Window Size
# -m sliding amount
# -l Experiment Length
# -d Distribution Type
# -c Number of change points
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CUSUM plotter')
    parser.add_argument('-w', '--window', action='store', dest='window_size', type=int)
    parser.add_argument('-m', '--movement', action='store', dest='slide_movement',type=int)
    parser.add_argument('-l', '--length', action='store', dest='length', type=int)
    parser.add_argument('-d', '--pile', action='store', dest='pile', type=int)
    parser.add_argument('-c', '--changePoints', action='store', dest='changePoints', type=int)
    parser.add_argument('directory',help='directory to use',action='store')
    parser.add_argument('-detrending',help='Types of Detrending',action='store', dest="detrend", type=int)
    args = parser.parse_args()
    length = 5400
    if args.length:
        length = args.length

    window_size = 60
    if args.window_size:
        window_size = args.window_size

    slide_movement = 10
    if args.slide_movement:
        slide_movement = args.slide_movement
    
    change_points=4
    if args.changePoints:
        change_points=args.changePoints 
        

    pile = 1
    if args.pile:
        pile = args.pile
    detrend = "constant"
    if args.detrend:
        detrend = args.detrend

    # print sys.argv[11] for printing the directory
    key_types = {'Distribution Type': int,
    'Ant ID': int,
    'Pile ID': int,
    'Y-Position': float,
    'Drop Off Time': float,
    'Pickup Time': float,
    'X-Position': float}

    path = sys.argv[13]+"CPFARecording"
    pathForPheromone=sys.argv[13]+"PheromoneRecordings/"
    # print pathForPheromone
    dirs = os.listdir( path )
    # For Saving Sliding Windows
    dirname = "./"+sys.argv[13]+"FilesForRScript"
    try:
        os.makedirs(dirname)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
                raise()
    #For Creating a directory to save plots
    dirname = "./"+sys.argv[13]+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_w"+str(window_size)+"_l"+str(length)+"_s"+str(slide_movement)+"_c"+str(change_points)+"_p"+str(pile)
    try:
        os.makedirs(dirname)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
                raise
    #print dirname
    # This would print all the files and directories
    for file in dirs:
        #print file
        splitter= file.split("_")
        #print splitter[1]
        with open(path+"/"+file, 'r') as csvfile:
            reader = csv.DictReader(csvfile.readlines(), delimiter="\t")
        
        reader = list(reader)
        data = {}
        for key in key_types:
            data[key] = []
            for row in reader:
                data[key].append(key_types[key](row[key]))
            
        dist_types = set(data['Distribution Type'])

    
        collection_times = {}
        sliding_windows = {}
        dataToWrite=[]
        for d in dist_types:
            collection_times[d] = np.zeros(length+1)
            sliding_windows[d] = []
        for d, t in zip(data['Distribution Type'], data['Drop Off Time']):
            if t >= 0:
                t = t 
                collection_times[d][t] += 1
    
        for i in xrange(0, int(length / slide_movement)):
            slmax = min(length,window_size + i * slide_movement)
            for d in dist_types:
                sl = collection_times[d][(i*slide_movement):slmax]
                sliding_windows[d].append(np.sum(sl))
        dataToWrite.append(0)
        for i in xrange(0, len(sliding_windows[pile])-1):
            if((sliding_windows[pile][i+1]-sliding_windows[pile][i])<0):
                dataToWrite.append(0)
            else:
                dataToWrite.append(sliding_windows[pile][i+1]-sliding_windows[pile][i])
        saveInto="./"+sys.argv[13]+"FilesForRScript/"+splitter[0]+"_"+splitter[1]+".txt"
        np.savetxt(saveInto,dataToWrite)
        proc=subprocess.Popen(["Rscript", "pyscripts/ChangePointDetector.R",saveInto,str(change_points),str(slide_movement),pathForPheromone,str(pile),dirname,str(detrend)])
        #break
        


