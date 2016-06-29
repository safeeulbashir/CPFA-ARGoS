from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import sys
import glob
import csv

def plot_iAnt_activities(directory):
    path=directory
    pheromoneFollowed=np.zeros(20)
    pheromoneLaid=np.zeros(20)
    siteFidelityFollowed=np.zeros(20)
    resourceDensity=np.zeros(20)
    key_types={'Resource Density': int,
    'Pheromone Laid': int,
    'Pheromone Followed':int,
    'Site Fidelity Followed':int
    }
    dirs=os.listdir(directory)
    for file in dirs:
        with open(directory+"/"+file,'r') as csvfile:
            reader=csv.DictReader(csvfile.readlines(),delimiter="\t")
        reader=list(reader)
        data={}
        for row in reader:
            #data[key]=[]
            for key in key_types:    
                #print "Resource Density  "+row['Resource Density']
                #if(int(row['Resource Density'])>0):
                    #print row['Resource Density']
                resourceDensity[int(row['Resource Density'])]=resourceDensity[int(row['Resource Density'])]+1
                pheromoneLaid[int(row['Resource Density'])]=pheromoneLaid[int(row['Resource Density'])]+int(row['Pheromone Laid'])
                pheromoneFollowed[int(row['Resource Density'])]=pheromoneFollowed[int(row['Resource Density'])]+int(row['Pheromone Followed'])
                siteFidelityFollowed[int(row['Resource Density'])]=siteFidelityFollowed[int(row['Resource Density'])]+int(row['Site Fidelity Followed'])
        #break
    print "Resource Density\t Resource Density Occurence\t Pheromone Laid\t Pheromone Followed\t SiteFidelity Followed"
    for x in range(0,19):
    	print repr(x).rjust(10),repr(resourceDensity[x]).rjust(10),repr(pheromoneLaid[x]).rjust(10),repr(pheromoneFollowed[x]).rjust(10),repr(siteFidelityFollowed[x]).rjust(10)

    #print pheromoneFollowed
    #print pheromoneLaid
    #print siteFidelityFollowed



if __name__ == "__main__":
    directory="CPFA_saves/ActivityData_Cluster/"
    #print directory
    plot_iAnt_activities(directory)