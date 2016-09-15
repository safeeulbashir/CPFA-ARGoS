import sys
import numpy as np
import os
Directory=str.split(sys.argv[1],"/")

pathToCPFARecordingDir="./"+Directory[0]+"/"+Directory[1]+"/"+"CPFARecording/"
dirs = os.listdir( pathToCPFARecordingDir )
RandomSeeds=list()
FromCP=list()
dirs2=os.listdir(sys.argv[1])
for file in dirs2:
	splitter=file.split("_")
	if(len(splitter)>1):
		splitter2=splitter[1].split(".")
		FromCP.append(splitter2[0])
for file in dirs:
	splitter= file.split("_")
	#print splitter[1]
	if(splitter[1] in FromCP):
		RandomSeeds.append(splitter[1])
	else:
		print splitter[1]

