import os
import errno

species="Maricopa"
if(species=="Rugosus"):
    print "Rugosus";
    NumberOfChangePoints=[4,4,4]
    RootDirectory="CPFA_saves/RugosusFieldData"
    ChangePointFiles=["CPFA_saves/RugosusFieldData/2016-12-02_05-04-11_w60_l5400_s10_c4_p1","CPFA_saves/RugosusFieldData/2016-12-02_05-04-32_w60_l5400_s10_c4_p4","CPFA_saves/RugosusFieldData/2016-12-02_05-04-57_w60_l5400_s10_c4_p16"]
elif(species=="Desertorum"):
    print "Desertorum"
    NumberOfChangePoints=[6,4,2]
    RootDirectory="CPFA_saves/DesertorumFieldData"
    ChangePointFiles=["CPFA_saves/DesertorumFieldData/2016-12-02_05-12-57_w60_l5400_s10_c6_p1","CPFA_saves/DesertorumFieldData/2016-12-02_05-24-10_w60_l5400_s10_c4_p4","CPFA_saves/DesertorumFieldData/2016-12-02_05-24-41_w60_l5400_s10_c2_p16"]
elif(species=="Maricopa"):
    print "Maricopa"
    NumberOfChangePoints=[2,5,4]
    RootDirectory="CPFA_saves/MaricopaFieldData"
    ChangePointFiles=["CPFA_saves/MaricopaFieldData/2016-12-02_05-06-13_w60_l5400_s10_c2_p1","CPFA_saves/MaricopaFieldData/2016-12-02_05-08-15_w60_l5400_s10_c5_p4","CPFA_saves/MaricopaFieldData/2016-12-02_05-10-08_w60_l5400_s10_c4_p16"]
Pile=[1,4,16]
AllChangePointSavingDirectory=os.path.join(RootDirectory,"AllPlots")
try:
    os.makedirs(AllChangePointSavingDirectory)
except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(AllChangePointSavingDirectory):
        pass
    else:
            raise
Indexer=0
counter=0
for file in ChangePointFiles:
	#print file
	ChangePointFileName=os.path.join(file,"ChangePoints.txt")
	FileToRead=open(ChangePointFileName,"r")
	CPfilename=""
	lines=FileToRead.readlines()
	for line in lines:
		if(counter==0): ##This is a file name
			CPfilename=line.replace("\n","")
			AppendTo=open(os.path.join(AllChangePointSavingDirectory,CPfilename), "a+")
			AppendTo.write(str(Pile[Indexer]))
			AppendTo.write(" ")
			#print "from first "+str(counter)+" "+CPfilename
			counter=counter+1
			#print NumberOfChangePoints[Indexer]
			#print "Creating File "+CPfilename 
		elif(counter<NumberOfChangePoints[Indexer]):
			number=line.replace("\n","")
			AppendTo.write(number)
			AppendTo.write(" ")
			#print counter
			#print "from second "+str(counter)+" "+number
			counter=counter+1
		elif(counter==NumberOfChangePoints[Indexer]):
			counter=0
			number=line.replace("\n","")
			AppendTo.write(number)
			#print "from third"+str(counter) 
			AppendTo.write("\n") 
			AppendTo.close()
		#print line.replace("\n","")
	Indexer=Indexer+1
