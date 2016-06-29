from lxml import etree
import numpy as np
import copy
import csv
import argparse
import numpy as np
import subprocess
import csv
import tempfile
import os
import datetime
import numpy as np
import time
import logging
from random import seed
import shutil
from posix import mkdir
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def load_xml_default():
    filename ='CPFAExampleEvolution.xml' #raw_input('Choose a file name(e.g. cluster_2_mac.argos)')
    name_and_extension = filename.split(".")
    fileFullPath = "./experiments/"+filename
    f= open(fileFullPath)
    content = f.readlines()
    result=""
    for line in content:
        result +=line
    return result, name_and_extension[0]

class ArgosRunException(Exception):
    pass

class DataGenerator():
    
    def __init__(self,experiments):
        self.seeds = [np.random.randint(2 ** 32) for _ in range(experiments)]
        self.save_dir = os.path.join("CPFA_saves", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.pheromoeRecodringDir=os.path.join(self.save_dir,"PheromoneRecordings")
        self.siteFidelityRecodringDir=os.path.join(self.save_dir,"SiteFidelityRecordings")
        self.CPFARecordingDir=os.path.join(self.save_dir,"CPFARecording")
        self.LINUX_CONTROLLER_LIB = "build/source/CPFA/libCPFA_controller"
        self.MAC_CONTROLLER_LIB = "build/source/CPFA/libCPFA_controller.dylib"
        self.LINUX_LOOP_LIB = "build/source/CPFA/libCPFA_loop_functions"
        self.MAC_LOOP_LIB = "build/source/CPFA/libCPFA_loop_functions.dylib"
        self.ARGOS_XML_DEFAULT, XML_FILE_NAME = load_xml_default()
        #print seeds
        #print "Dishkiao"
    def runSimulation(self):
        mkdir_p(self.save_dir)
        mkdir_p(self.pheromoeRecodringDir)
        mkdir_p(self.CPFARecordingDir)
        mkdir_p(self.siteFidelityRecodringDir)
        for seed in self.seeds:
            #print seed
            argos_xml = etree.fromstring(self.ARGOS_XML_DEFAULT)
            attrib = argos_xml.find("framework").find("experiment").attrib
            attrib.update({"random_seed": str(int(seed))})
            xml_str = etree.tostring(argos_xml)
            cwd = os.getcwd()
            tmpf = tempfile.NamedTemporaryFile('w', suffix=".argos", prefix="gatmp",
                                               dir=os.path.join(cwd, "experiments"),
                                               delete=False)
            tmpf.write(xml_str)
            tmpf.close()
            argos_args = ["argos3", "-n", "-c", tmpf.name]
            argos_run = subprocess.Popen(argos_args, stdout=subprocess.PIPE)
            #Wait until argos is finished
            while argos_run.poll() is None:
                time.sleep(0.5)
            if argos_run.returncode != 0:
                logging.error("Argos failed test")
                # when argos fails just return fitness 0
                return 0
	    lines = argos_run.stdout.readlines()
            os.unlink(tmpf.name)
            print lines[-1]
            #return int(lines[-1].strip().split(",")[0])
            cwd=os.getcwd()
            dir=os.path.join(self.save_dir,"RandomSeed_"+str(seed))
            
            shutil.copyfile("iAntFoodPosition.txt", self.CPFARecordingDir+"/RandomSeed_"+str(seed)+"_iAntFoodPosition.txt")
            shutil.copyfile("AllPheromoneTrailData.txt",self.pheromoeRecodringDir+"/RandomSeed_"+str(seed)+".pheromone")
            #shutil.copyfile("AllSiteFidelityData.txt",self.siteFidelityRecodringDir+"/RandomSeed_"+str(seed)+".siteFidelity")
	    print "CPFA data recorded for Seed Distribution "+str(seed)+"\n"

#if __name__ == "__main__":
parser = argparse.ArgumentParser(description='CPFA XML printer')
parser.add_argument('-e', '--experiments', action='store', dest='experiments', required=True)
args = parser.parse_args()
experiments = args.experiments
myFirstObject=DataGenerator(int(experiments))
print "Initiating "+experiments+" Experiments Using the Best parameters. "
myFirstObject.runSimulation()
