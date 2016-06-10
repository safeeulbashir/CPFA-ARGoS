#!/bin/bash
# First argument is the number of processes to generate

nohup bash -c "mpirun -n $1 -machinefile $2 ~/Documents/ForEvaluation/CPFA-ARGoS/build/cpfa_evolver -t 90 -p 50 -g 100 -c 0.1 -m 0.1 -s 0.2 -e 1 -x experiments/CPFAExampleEvolution.xml seed 1111 && cat example_evolution_output.txt  > evolve_clustered.out &

