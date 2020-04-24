#!/usr/bin/env python3

import sys
import copy
import time
import random

from DataPkg.InputData import InputData as InD
from DataPkg.OutputData import OutputData as OutD


# Load all the arguments in their respective variables
in_file   = sys.argv[1]
out_file  = sys.argv[2]
time_lim  = int(sys.argv[3])
rand_seed = int(sys.argv[4])
threads   = int(sys.argv[5])

# Initialise the random seed using the given value
random.seed(rand_seed)

# Create an InputData element and load the data from a csv file.
ind = InD()
ind.loadCSV(in_file)

# Create an OutputData element and initialise it using the loaded input data
outd = OutD()
outd.initialise(ind)
outd2=copy.deepcopy(outd)   # Copy the initial solution to start local search

# Find the starting time of the program, so the time limit can be ensured
timeout_start = time.time()
idx = 0

while time.time() < timeout_start + time_lim:   # Run as long as the time limit is not exceeded
    idx += 1
    outd2.localSearch()     # Execute a local search function
    if outd.getCost() > outd2.getCost():    # If the cost is better ...
        outd = copy.deepcopy(outd2)         # Copy the new solution to the best solution
        print('Best', outd2.getCost())
    else:                                   # Otherwise ...
        outd2 = copy.deepcopy(outd)         # Go back an do another search

# Save the solution as a csv file
outd.saveCSV(out_file)
print("Iter:", idx)