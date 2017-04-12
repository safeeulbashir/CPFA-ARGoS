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


print sys.argv[2],sys.argv[3],sys.argv[4]

PathToCPs=[]
PathToCPs.append(os.path.join(sys.argv[2],""))
PathToCPs.append(os.path.join(sys.argv[3],""))
PathToCPs.append(os.path.join(sys.argv[4],""))
AllChangePointSavingDirectory=os.path.join(sys.argv[1],"AllPlots") # DefineRootDirectory
try:
    os.makedirs(AllChangePointSavingDirectory)
except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(AllChangePointSavingDirectory):
        pass
    else:
            raise
Pile=[1,4,16]
Indexer=0
counter=0
for file in PathToCPs:
	#print file
	ChangePointFileName=os.path.join(file,"ChangePoints.txt")
	FileToRead=open(ChangePointFileName,"r")
	CPfilename=""
	lines=FileToRead.readlines()
	for line in lines:
		#print line
		LineSplit=line.split("\t")
		CPfilename=LineSplit[0]+".txt"
		AppendTo=open(os.path.join(AllChangePointSavingDirectory,CPfilename), "a+")
		for values in LineSplit:
			if(values==LineSplit[0]):
				#print "Akaimma"
				AppendTo.write(str(Pile[Indexer]))
				AppendTo.write(" ")
			else:
				AppendTo.write(values.replace("\n",""))
				AppendTo.write(" ")
		AppendTo.write("\n") 
		AppendTo.close()
		print LineSplit[0]
	Indexer=Indexer+1


