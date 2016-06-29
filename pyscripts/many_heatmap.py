import sys
import glob
import os
import argos_util
import re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import argparse
import numpy as np

def plot_param_vs_fitness(param, files, threshold=0):
    number_re = re.compile(r'\d+')
    populations = {}
    for genfile in files:
        gen_number = int(number_re.findall(os.path.basename(genfile))[0])
        if gen_number in populations:
            populations[gen_number].extend(argos_util.read_pop_from_csv(genfile))
        else:
            populations[gen_number] = argos_util.read_pop_from_csv(genfile)

    gens = range(len(populations.keys()))

    fitness = []
    paramvals = []

    threshold = float(threshold)
    for g in gens:
        for p in populations[g]:
            if float(p["fitness"]) > threshold:
                fitness.append(float(p["fitness"]))
                paramvals.append(float(p[param]))

    paramvals = np.array(paramvals)
    fitness = np.array(fitness)
    matplotlib.rcParams.update({'font.size': 16})
    plt.hist2d(paramvals, fitness, bins=20,
               range=[[argos_util.CPFA_LIMITS[param][0],argos_util.CPFA_LIMITS[param][1]],[threshold,725]],cmap='Greens')
    plt.colorbar()
    plt.ylabel('fitness (seeds collected)')
    plt.xlabel(param)
    plt.savefig(param+"_many.pdf")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GA plotter')
    parser.add_argument('-p', '--param', action='store', dest='param', help='Param to plot', required=True)
    parser.add_argument('-t', '--threshold', action='store', dest='threshold', help='Param to plot')
    parser.add_argument('directories', nargs='*', action='store')

    args = parser.parse_args()

    directories = args.directories
    files = []
    for directory in directories:
        files.extend(glob.glob(os.path.join(directory, "*.gapy")))

    threshold = 0
    if args.threshold:
        threshold = args.threshold


    if args.param:
        plot_param_vs_fitness(args.param, files, threshold)
